######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 16:35
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Generator
from airquality.extra.timest import Timest
from airquality.iterables.abc import IterableItemsABC
from airquality.datamodel.geometry import PostgisPoint, NullGeometry
from airquality.datamodel.requests import AddFixedSensorRequest, Channel, AddSensorMeasureRequest, AddPlaceRequest, \
    WeatherConditionsRequest, AddWeatherDataRequest, WeatherAlertRequest


_PURPLEAIR_TYPE = 'Purpleair/Thingspeak'

_CHANNEL_1A = {'key': 'primary_key_a', 'ident': 'primary_id_a', 'name': '1A'}
_CHANNEL_1B = {'key': 'primary_key_b', 'ident': 'primary_id_b', 'name': '1B'}
_CHANNEL_2A = {'key': 'secondary_key_a', 'ident': 'secondary_id_a', 'name': '2A'}
_CHANNEL_2B = {'key': 'secondary_key_b', 'ident': 'secondary_id_b', 'name': '2B'}
_PURPLEAIR_API_PARAM = [_CHANNEL_1A, _CHANNEL_1B, _CHANNEL_2A, _CHANNEL_2B]


class PurpleairIterableRequests(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and defines the business rules for converting a
    *PurpleairDM* into an *AddFixedSensorRequest*
    """

    def __init__(self, datamodels: IterableItemsABC, timest: Timest):
        self._datamodels = datamodels
        self._timest = timest

    def items(self) -> Generator:
        for dm in self._datamodels:
            created_at = self._timest.utc_time2utc_localtz(
                time=dm.date_created, latitude=dm.latitude, longitude=dm.longitude
            )
            channels = [Channel(api_key=getattr(dm, ch['key']),
                                api_id=str(getattr(dm, ch['ident'])),
                                channel_name=ch['name'],
                                last_acquisition=created_at) for ch in _PURPLEAIR_API_PARAM]
            sensor_name = f"{dm.name} ({dm.sensor_index})"
            yield AddFixedSensorRequest(
                type=_PURPLEAIR_TYPE, name=sensor_name, channels=channels
            )


class AtmotubeIterableRequests(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and defines the business rules for converting a
    *AtmotubeDM* into an *AddSensorMeasureRequest*
    """

    def __init__(self, datamodels: IterableItemsABC, timest: Timest, measure_param: Dict[str, int]):
        self._timest = timest
        self._datamodels = datamodels
        self._measure_param = measure_param

    def items(self) -> Generator:
        for dm in self._datamodels:
            coords = dm.coords

            geolocation = NullGeometry()
            timestamp = self._timest.utc_time2utc_tz(dm.time)
            if coords is not None:
                lat = coords['lat']
                lng = coords['lon']
                geolocation = PostgisPoint(latitude=lat, longitude=lng)
                timestamp = self._timest.utc_time2utc_localtz(time=dm.time, latitude=lat, longitude=lng)

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

    def __init__(
        self,
        timest: Timest,
        datamodels: IterableItemsABC,
        measure_param: Dict[str, int],
        api_field_names: Dict[str, str]
    ):
        self._timest = timest
        self._datamodels = datamodels
        self._measure_param = measure_param
        self._api_field_names = api_field_names

    def items(self):
        for dm in self._datamodels:
            yield AddSensorMeasureRequest(
                timestamp=self._timest.utc_time2utc_localtz(time=dm.created_at),
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


class AddOpenWeatherMapDataRequestBuilder(IterableItemsABC):
    def __init__(
        self,
        timest: Timest,
        datamodels: IterableItemsABC,
        weather_map: Dict[int, Dict[str, int]]
    ):
        self._timest = timest
        self.datamodels = datamodels
        self.weather_map = weather_map

    def items(self):
        for dm in self.datamodels:
            yield AddWeatherDataRequest(
                current=self._request_of(source=dm.current, tzname=dm.tz_name),
                hourly=[self._request_of(source=item, tzname=dm.tz_name) for item in dm.hourly_forecast],
                daily=[self._request_of(source=item, tzname=dm.tz_name) for item in dm.daily_forecast],
                alerts=[self._alert_of(source=item, tzname=dm.tz_name) for item in dm.alerts]
            )

    def _alert_of(self, source, tzname: str) -> WeatherAlertRequest:
        return WeatherAlertRequest(
            sender_name=source.sender_name,
            alert_event=source.alert_event,
            alert_begin=self._safe_time(time=source.alert_begin, tzname=tzname),
            alert_until=self._safe_time(time=source.alert_until, tzname=tzname),
            description=source.description
        )

    def _request_of(self, source, tzname: str) -> WeatherConditionsRequest:
        weather = source.weather[0]             # take only the first weather instance from the list.
        return WeatherConditionsRequest(
            timestamp=self._timest.utc_time2utc_localtz(time=source.dt, tzname=tzname),
            sunrise=self._safe_time(time=source.sunrise, tzname=tzname),
            sunset=self._safe_time(time=source.sunset, tzname=tzname),
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
            weather_id=self.weather_map[weather.id][weather.icon]
        )

    def _safe_time(self, time, tzname: str):
        if time is not None:
            return self._timest.utc_time2utc_localtz(time=time, tzname=tzname)
        return None
