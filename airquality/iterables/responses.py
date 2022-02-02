######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 18:54
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from itertools import count
from typing import Generator, List
from airquality.iterables.abc import IterableItemsABC
from airquality.datamodel.responses import AddFixedSensorResponse, AddSensorMeasureResponse, \
    AddPlaceResponse, AddWeatherDataResponse


class FixedSensorIterableResponses(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and defines the business rules for converting
    an *AddFixedSensorRequest* object into *AddFixedSensorResponse* object.
    """

    def __init__(
        self,
        start_sensor_id: int,
        requests: IterableItemsABC,
    ):
        self._requests = requests
        self._start_sensor_id = start_sensor_id

    def items(self) -> Generator[AddFixedSensorResponse, None, None]:
        sensor_id_counter = count(self._start_sensor_id)
        for req in self._requests:
            sensor_id = next(sensor_id_counter)
            yield AddFixedSensorResponse(
                sensor_record=f"({sensor_id}, '{req.type}', '{req.name}')",
                apiparam_record=','.join(f"({sensor_id}, '{ch.api_key}', "
                                         f"'{ch.api_id}', '{ch.channel_name}', "
                                         f"'{ch.last_acquisition}')" for ch in req.channels)
            )


class MobileMeasureIterableResponses(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and defines the business rules for converting
    an *AddSensorMeasureRequest* object into *AddSensorMeasureResponse* object for mobile sensors.
    """

    def __init__(
        self,
        start_packet_id: int,
        requests: IterableItemsABC
    ):
        self.requests = requests
        self.start_packet_id = start_packet_id

    def items(self) -> Generator[AddSensorMeasureResponse, None, None]:
        packet_id_counter = count(self.start_packet_id)
        for req in self.requests:
            ts = req.timestamp
            geo = req.geolocation
            packet_id = next(packet_id_counter)
            yield AddSensorMeasureResponse(
                measure_record=','.join(f"({packet_id}, {param_id}, {param_val}, '{ts}', {geo})"
                                        for param_id, param_val in req.measures)
            )


class StationMeasureIterableResponses(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and defines the business rules for converting
    an *AddSensorMeasureRequest* object into *AddSensorMeasureResponse* object for fixed sensors.
    """

    def __init__(
        self,
        sensor_id: int,
        start_packet_id: int,
        requests: IterableItemsABC,
    ):
        self._requests = requests
        self._sensor_id = sensor_id
        self._start_packet_id = start_packet_id

    def items(self) -> Generator:
        packet_id_counter = count(self._start_packet_id)
        for req in self._requests:
            ts = req.timestamp
            packet_id = next(packet_id_counter)
            yield AddSensorMeasureResponse(
                measure_record=','.join(f"({packet_id}, {self._sensor_id}, {param_id}, {param_val}, '{ts}')"
                                        for param_id, param_val in req.measures)
            )


class AddPlaceIterableResponses(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and defines the business rules for converting
    an *AddPlaceRequest* object into *AddPlaceResponse* object for fixed sensors.
    """

    def __init__(self, requests: IterableItemsABC):
        self.requests = requests

    def items(self):
        for req in self.requests:
            yield AddPlaceResponse(
                place_record=f"('{req.poscode}', '{req.countrycode}', "
                             f"'{req.placename}', '{req.province}', "
                             f"'{req.state}', {req.geolocation})"
            )


def _safe_sql_value_of(val) -> str:
    if not isinstance(val, (float, int, type(None))):
        val = f"'{val}'"
    return val if val is not None else "NULL"


def _body_of(source, attributes: List[str]):
    return ', '.join(f"{_safe_sql_value_of(getattr(source, attr))}" for attr in attributes)


class WeatherDataIterableResponses(IterableItemsABC):

    DAILY_ATTRIBUTES = ['weather_id', 'temperature', 'min_temp', 'max_temp', 'pressure', 'humidity', 'wind_speed', 'wind_direction', 'rain', 'pop', 'snow', 'timestamp']
    HOURLY_ATTRIBUTES = ['weather_id', 'temperature', 'pressure', 'humidity', 'wind_speed', 'wind_direction', 'rain', 'pop', 'snow', 'timestamp']
    CURRENT_ATTRIBUTES = ['weather_id', 'temperature', 'pressure', 'humidity', 'wind_speed', 'wind_direction', 'rain', 'snow', 'timestamp', 'sunrise', 'sunset']
    ALERT_ATTRIBUTES = ['sender_name', 'alert_event', 'alert_begin', 'alert_until', 'description']

    def __init__(
        self,
        geoarea_id: int,
        requests: IterableItemsABC
    ):
        self.requests = requests
        self.geoarea_id = geoarea_id

    def items(self) -> Generator:
        for req in self.requests:
            yield AddWeatherDataResponse(
                current_weather_record=self._record_of(body=_body_of(source=req.current, attributes=self.CURRENT_ATTRIBUTES)),
                hourly_forecast_record=','.join(self._record_of(body=_body_of(source=item, attributes=self.HOURLY_ATTRIBUTES)) for item in req.hourly),
                daily_forecast_record=','.join(self._record_of(body=_body_of(source=item, attributes=self.DAILY_ATTRIBUTES)) for item in req.daily),
                weather_alert_record=','.join(self._record_of(body=_body_of(source=item, attributes=self.ALERT_ATTRIBUTES)) for item in req.alerts)
            )

    def _record_of(self, body: str) -> str:
        return f"({self.geoarea_id}, {body})"
