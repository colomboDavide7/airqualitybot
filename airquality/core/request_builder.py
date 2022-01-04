######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 16:35
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.datamodel.request import AddFixedSensorsRequest, AddMobileMeasuresRequest, \
    AddSensorMeasuresRequest, Channel, AddPlacesRequest, AddWeatherForecastRequest, AddOpenWeatherMapDataRequest
from airquality.datamodel.geometry import PostgisPoint, NullGeometry
from airquality.core.iteritems import IterableItemsABC
from typing import Dict, Generator
from datetime import datetime


class AddPurpleairSensorRequestBuilder(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules for translating
    a set of *PurpleairDatamodel* items into an *AddFixedSensorRequest* Generator.
    """

    def __init__(self, datamodel: IterableItemsABC):
        self.datamodel = datamodel

    def items(self) -> Generator[AddFixedSensorsRequest, None, None]:
        for dm in self.datamodel:
            created_at = datetime.fromtimestamp(dm.date_created)
            channels = [
                Channel(api_key=dm.primary_key_a, api_id=str(dm.primary_id_a), channel_name="1A",
                        last_acquisition=created_at),
                Channel(api_key=dm.primary_key_b, api_id=str(dm.primary_id_b), channel_name="1B",
                        last_acquisition=created_at),
                Channel(api_key=dm.secondary_key_a, api_id=str(dm.secondary_id_a), channel_name="2A",
                        last_acquisition=created_at),
                Channel(api_key=dm.secondary_key_b, api_id=str(dm.secondary_id_b), channel_name="2B",
                        last_acquisition=created_at)
            ]
            yield AddFixedSensorsRequest(
                type="Purpleair/Thingspeak",
                name=f"{dm.name} ({dm.sensor_index})",
                channels=channels,
                geolocation=PostgisPoint(latitude=dm.latitude, longitude=dm.longitude)
            )


class AddAtmotubeMeasureRequestBuilder(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules for translating
    a set of *AtmotubeDatamodel* items into an *AddMobileMeasureRequest* Generator.
    """

    TIMESTAMP_FMT = "%Y-%m-%dT%H:%M:%S.000Z"

    def __init__(self, datamodel: IterableItemsABC, code2id: Dict[str, int]):
        self.datamodel = datamodel
        self.code2id = code2id

    def items(self) -> Generator[AddMobileMeasuresRequest, None, None]:
        for dm in self.datamodel:
            pt = dm.coords
            yield AddMobileMeasuresRequest(
                timestamp=datetime.strptime(dm.time, self.TIMESTAMP_FMT),
                geolocation=NullGeometry() if pt is None else PostgisPoint(latitude=pt['lat'], longitude=pt['lon']),
                measures=[(ident, getattr(dm, code)) for code, ident in self.code2id.items() if
                          getattr(dm, code) is not None]
            )


class AddThingspeakMeasuresRequestBuilder(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules for translating
    a set of *ThingspeakAPIData* items into an *AddStationMeasuresRequest* generator.
    """

    TIMESTAMP_FMT = "%Y-%m-%dT%H:%M:%SZ"

    def __init__(self, datamodel: IterableItemsABC, code2id: Dict[str, int], field_map: Dict[str, str]):
        self.datamodel = datamodel
        self.code2id = code2id
        self.field_map = field_map

    def items(self):
        for dm in self.datamodel:
            yield AddSensorMeasuresRequest(
                timestamp=datetime.strptime(dm.created_at, self.TIMESTAMP_FMT),
                measures=[(self.code2id[fcode], getattr(dm, fname)) for fname, fcode in self.field_map.items() if
                          getattr(dm, fname) is not None]
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

    def __init__(self, datamodels: IterableItemsABC, weather_map: Dict[int, Dict[str, int]]):
        self.datamodels = datamodels
        self.weather_map = weather_map

    def items(self):
        for dm in self.datamodels:
            yield AddOpenWeatherMapDataRequest(
                current=self.request_of(source=dm.current),
                hourly=[self.request_of(source=item) for item in dm.hourly_forecast],
                daily=[self.request_of(source=item) for item in dm.daily_forecast]
            )

    def request_of(self, source) -> AddWeatherForecastRequest:
        weather = source.weather[0]
        return AddWeatherForecastRequest(
            timestamp=datetime.utcfromtimestamp(source.dt),
            temperature=source.temp,
            min_temp=source.temp_min,
            max_temp=source.temp_max,
            pressure=source.pressure,
            humidity=source.humidity,
            wind_speed=source.wind_speed,
            wind_direction=source.wind_deg,
            rain=source.rain,
            snow=source.snow,
            weather_id=self.weather_map[weather.id][weather.icon]
        )
