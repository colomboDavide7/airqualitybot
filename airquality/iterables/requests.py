######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 16:35
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Generator
import airquality.extra.timest as timest
from airquality.iterables.abc import IterableItemsABC
from airquality.datamodel.geometry import PostgisPoint, NullGeometry
from airquality.datamodel.requests import WeatherConditionsRequest, AddWeatherDataRequest, WeatherAlertRequest, \
    AddFixedSensorRequest, SensorChannelParam, AddSensorMeasureRequest, AddPlaceRequest


class PurpleairIterableRequests(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and defines the business rules for converting a
    *PurpleairDM* into an *AddFixedSensorRequest*
    """

    _PURPLEAIR_TYPE = 'Purpleair/Thingspeak'

    _CHANNEL_1A = {'key': 'primary_key_a', 'ident': 'primary_id_a', 'name': '1A'}
    _CHANNEL_1B = {'key': 'primary_key_b', 'ident': 'primary_id_b', 'name': '1B'}
    _CHANNEL_2A = {'key': 'secondary_key_a', 'ident': 'secondary_id_a', 'name': '2A'}
    _CHANNEL_2B = {'key': 'secondary_key_b', 'ident': 'secondary_id_b', 'name': '2B'}
    _PURPLEAIR_API_PARAM = [_CHANNEL_1A, _CHANNEL_1B, _CHANNEL_2A, _CHANNEL_2B]

    def __init__(self, datamodels: IterableItemsABC):
        self._datamodels = datamodels
        self._timest = timest

    def items(self) -> Generator:
        for dm in self._datamodels:
            created_at = timest.make_timezone_aware_FROM_COORDS(utctime=dm.date_created,
                                                                latitude=dm.latitude,
                                                                longitude=dm.longitude)
            channel_param = [SensorChannelParam(api_key=getattr(dm, ch['key']),
                                                api_id=str(getattr(dm, ch['ident'])),
                                                channel_name=ch['name'],
                                                last_acquisition=created_at) for ch in self._PURPLEAIR_API_PARAM]
            yield AddFixedSensorRequest(name=f"{dm.name} ({dm.sensor_index})",
                                        type=self._PURPLEAIR_TYPE,
                                        channel_param=channel_param)


class AtmotubeIterableRequests(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and defines the business rules for converting a
    *AtmotubeDM* into an *AddSensorMeasureRequest*
    """

    _TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

    def __init__(self, datamodels: IterableItemsABC, measure_param: Dict[str, int]):
        self._datamodels = datamodels
        self._measure_param = measure_param

    def items(self) -> Generator:
        for dm in self._datamodels:
            coords = dm.coords

            geolocation = NullGeometry()
            timestamp = timest.make_timezone_aware_UTC(dm.time, fmt=self._TIME_FORMAT)
            if coords is not None:
                lat = coords['lat']
                lng = coords['lon']
                geolocation = PostgisPoint(latitude=lat, longitude=lng)
                timestamp = timest.make_timezone_aware_FROM_COORDS(
                    utctime=dm.time, latitude=lat, longitude=lng, fmt=self._TIME_FORMAT
                )

            yield AddSensorMeasureRequest(
                timestamp=timestamp,
                geolocation=geolocation,
                measures=[(ident, getattr(dm, code))
                          for code, ident in self._measure_param.items()
                          if getattr(dm, code) is not None]
            )


class ThingspeakIterableRequests(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and defines the business rules for converting a
    *ThingspeakDM* into an *AddSensorMeasureRequest*
    """

    _TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def __init__(self, datamodels: IterableItemsABC, measure_param: Dict[str, int], api_field_names: Dict[str, str]):
        self._datamodels = datamodels
        self._measure_param = measure_param
        self._api_field_names = api_field_names

    def items(self):
        for dm in self._datamodels:
            yield AddSensorMeasureRequest(
                timestamp=timest.make_timezone_aware_FROM_LOCAL(utctime=dm.created_at, fmt=self._TIME_FORMAT),
                measures=[(self._measure_param[fcode], getattr(dm, fname))
                          for fname, fcode in self._api_field_names.items()
                          if getattr(dm, fname) is not None]
            )


class GeonamesIterableRequests(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and defines the business rules for converting a
    *GeonamesDM* into an *AddPlaceRequest*
    """

    def __init__(self, datamodels: IterableItemsABC):
        self._datamodels = datamodels

    def items(self):
        for dm in self._datamodels:
            yield AddPlaceRequest(
                placename=dm.place_name,
                poscode=dm.postal_code,
                countrycode=dm.country_code,
                state=dm.state,
                province=dm.province,
                geolocation=PostgisPoint(latitude=dm.latitude, longitude=dm.longitude)
            )


def _safe_make_timezone_aware_datetime_from_unix_timestamp(unixts: int, tzname: str):
    if unixts is not None:
        return timest.make_timezone_aware_FROM_NAME(utctime=unixts, timezone_name=tzname)
    return None


def _alert_of(source, tzname: str) -> WeatherAlertRequest:
    return WeatherAlertRequest(
        sender=source.sender_name,
        event=source.alert_event,
        begin=_safe_make_timezone_aware_datetime_from_unix_timestamp(unixts=source.alert_begin, tzname=tzname),
        until=_safe_make_timezone_aware_datetime_from_unix_timestamp(unixts=source.alert_until, tzname=tzname),
        description=source.description
    )


class OpenweathermapIterableRequests(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and defines the business rules for converting a
    *OpenweathermapDM* into an *AddWeatherDataRequest*
    """

    def __init__(self, datamodels: IterableItemsABC, weather_map: Dict[str, int]):
        self.datamodels = datamodels
        self.weather_map = weather_map

    def items(self):
        for dm in self.datamodels:
            yield AddWeatherDataRequest(
                current=self._request_of(source=dm.current, tzname=dm.tz_name),
                hourly=[self._request_of(source=item, tzname=dm.tz_name) for item in dm.hourly_forecast],
                daily=[self._request_of(source=item, tzname=dm.tz_name) for item in dm.daily_forecast],
                alerts=[_alert_of(source=item, tzname=dm.tz_name) for item in dm.alerts]
            )

    def _request_of(self, source, tzname: str) -> WeatherConditionsRequest:
        weather = source.weather[0]             # take only the first weather instance from the list.
        return WeatherConditionsRequest(
            timestamp=_safe_make_timezone_aware_datetime_from_unix_timestamp(unixts=source.dt, tzname=tzname),
            sunrise=_safe_make_timezone_aware_datetime_from_unix_timestamp(unixts=source.sunrise, tzname=tzname),
            sunset=_safe_make_timezone_aware_datetime_from_unix_timestamp(unixts=source.sunset, tzname=tzname),
            temperature=source.temp,
            min_temp=source.temp_min,
            max_temp=source.temp_max,
            pressure=source.pressure,
            humidity=source.humidity,
            wind_speed=source.wind_speed,
            wind_direction=source.wind_deg,
            rain=source.rain,
            pop=source.pop,
            snow=source.snow,
            weather_id=self.weather_map[f"{weather.id}_{weather.icon}"]
        )
