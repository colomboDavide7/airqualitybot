######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 16:35
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Generator
from airquality.extra.timest import Timest
from airquality.core.iteritems import IterableItemsABC
from airquality.datamodel.geometry import PostgisPoint, NullGeometry
from airquality.datamodel.request import AddFixedSensorsRequest, \
    AddMobileMeasuresRequest, \
    AddSensorMeasuresRequest, Channel, \
    AddPlacesRequest, \
    AddWeatherForecastRequest, \
    AddOpenWeatherMapDataRequest, \
    AddWeatherAlertRequest


class AddPurpleairSensorRequestBuilder(IterableItemsABC):
    """
    A subclass of *IterableItemsABC* that defines the business rules for translating
    a set of *PurpleairDatamodel* items into an *AddFixedSensorRequest* Generator.
    """

    def __init__(self, datamodel: IterableItemsABC, timest: Timest):
        self.datamodel = datamodel
        self._timest = timest

    def items(self) -> Generator[AddFixedSensorsRequest, None, None]:
        for dm in self.datamodel:
            created_at = self._timest.utc_time2utc_localtz(
                time=dm.date_created, latitude=dm.latitude, longitude=dm.longitude
            )

            channels = [Channel(api_key=dm.primary_key_a,
                                api_id=str(dm.primary_id_a),
                                channel_name="1A",
                                last_acquisition=created_at),
                        Channel(api_key=dm.primary_key_b,
                                api_id=str(dm.primary_id_b),
                                channel_name="1B",
                                last_acquisition=created_at),
                        Channel(api_key=dm.secondary_key_a,
                                api_id=str(dm.secondary_id_a),
                                channel_name="2A",
                                last_acquisition=created_at),
                        Channel(api_key=dm.secondary_key_b,
                                api_id=str(dm.secondary_id_b),
                                channel_name="2B",
                                last_acquisition=created_at)]
            yield AddFixedSensorsRequest(
                type="Purpleair/Thingspeak",
                name=f"{dm.name} ({dm.sensor_index})",
                channels=channels
            )


class AddAtmotubeMeasureRequestBuilder(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules for translating
    a set of *AtmotubeDatamodel* items into an *AddMobileMeasureRequest* Generator.
    """

    TIMESTAMP_FMT = "%Y-%m-%dT%H:%M:%S.000Z"

    def __init__(self, datamodel: IterableItemsABC, timest: Timest, code2id: Dict[str, int]):
        self.datamodel = datamodel
        self._timest = timest
        self.code2id = code2id

    def items(self) -> Generator[AddMobileMeasuresRequest, None, None]:
        for dm in self.datamodel:
            pt = dm.coords
            yield AddMobileMeasuresRequest(
                timestamp=self._timest.utc_time2utc_tz(dm.time) if pt is None else
                          self._timest.utc_time2utc_localtz(time=dm.time, latitude=pt['lat'], longitude=pt['lon']),
                geolocation=NullGeometry() if pt is None else
                            PostgisPoint(latitude=pt['lat'], longitude=pt['lon']),
                measures=[(ident, getattr(dm, code)) for code, ident in self.code2id.items() if
                          getattr(dm, code) is not None]
            )


class AddThingspeakMeasuresRequestBuilder(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules for translating
    a set of *ThingspeakAPIData* items into an *AddStationMeasuresRequest* generator.
    """

    TIMESTAMP_FMT = "%Y-%m-%dT%H:%M:%SZ"

    def __init__(self, datamodel: IterableItemsABC, timest: Timest, code2id: Dict[str, int], field_map: Dict[str, str]):
        self.datamodel = datamodel
        self._timest = timest
        self.code2id = code2id
        self.field_map = field_map

    def items(self):
        for dm in self.datamodel:
            yield AddSensorMeasuresRequest(
                timestamp=self._timest.utc_time2utc_localtz(time=dm.created_at),
                measures=[
                    (self.code2id[fcode], getattr(dm, fname)) for
                    fname, fcode in self.field_map.items() if
                    getattr(dm, fname) is not None
                ]
            )


class AddPlacesRequestBuilder(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules for translating
    a set of *GeonamesData* into an *AddPlacesRequest* generator.
    """

    WGS84_SRID = 4326

    def __init__(self, datamodels: IterableItemsABC):
        self.datamodels = datamodels

    def items(self):
        for dm in self.datamodels:
            yield AddPlacesRequest(
                placename=dm.place_name,
                poscode=dm.postal_code,
                countrycode=dm.country_code,
                state=dm.state,
                province=dm.province,
                geolocation=PostgisPoint(latitude=dm.latitude, longitude=dm.longitude, srid=self.WGS84_SRID)
            )


class AddOpenWeatherMapDataRequestBuilder(IterableItemsABC):
    def __init__(self, datamodels: IterableItemsABC, timest: Timest, weather_map: Dict[int, Dict[str, int]]):
        self.datamodels = datamodels
        self.weather_map = weather_map
        self._timest = timest

    def items(self):
        for dm in self.datamodels:
            yield AddOpenWeatherMapDataRequest(
                current=self.request_of(source=dm.current, tzname=dm.tz_name),
                hourly=[self.request_of(source=item, tzname=dm.tz_name) for item in dm.hourly_forecast],
                daily=[self.request_of(source=item, tzname=dm.tz_name) for item in dm.daily_forecast],
                alerts=[self._alert_of(source=item, tzname=dm.tz_name) for item in dm.alerts]
            )

    def _alert_of(self, source, tzname: str) -> AddWeatherAlertRequest:
        return AddWeatherAlertRequest(
            sender_name=source.sender_name,
            alert_event=source.alert_event,
            alert_begin=self._safe_time(time=source.alert_begin, tzname=tzname),
            alert_until=self._safe_time(time=source.alert_until, tzname=tzname),
            description=source.description
        )

    def request_of(self, source, tzname: str) -> AddWeatherForecastRequest:
        weather = source.weather[0]             # take only the first weather instance from the list.
        return AddWeatherForecastRequest(
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
