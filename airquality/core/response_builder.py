######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 18:54
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from itertools import count
from typing import Generator, List
from airquality.core.iteritems import IterableItemsABC
from airquality.datamodel.request import AddFixedSensorsRequest, AddMobileMeasuresRequest, AddSensorMeasuresRequest
from airquality.datamodel.response import AddFixedSensorResponse, AddMobileMeasureResponse, AddStationMeasuresResponse,\
    AddPlacesResponse, AddOpenWeatherMapDataResponse


def apiparam_record(sensor_id: int, request: AddFixedSensorsRequest) -> str:
    return ','.join(f"({sensor_id}, '{ch.api_key}', '{ch.api_id}', '{ch.channel_name}', '{ch.last_acquisition}')"
                    for ch in request.channels)


class AddFixedSensorResponseBuilder(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules for
    translating a set of *AddFixedSensorRequest* items into
    an *AddFixedSensorResponse* Generator.
    """

    def __init__(
            self,
            requests: IterableItemsABC,         # The class that holds the requests items.
            start_sensor_id: int                # The database sensor id from where start to count the sensors.
    ):
        self.requests = requests
        self.start_sensor_id = start_sensor_id

    def items(self) -> Generator[AddFixedSensorResponse, None, None]:
        sensor_id_counter = count(self.start_sensor_id)
        for req in self.requests:
            sensor_id = next(sensor_id_counter)
            yield AddFixedSensorResponse(
                sensor_record=f"({sensor_id}, '{req.type}', '{req.name}')",
                apiparam_record=apiparam_record(sensor_id=sensor_id, request=req)
            )


def mobile_measure_record(packet_id: int, request: AddMobileMeasuresRequest) -> str:
    ts = request.timestamp
    g = request.geolocation
    return ','.join(f"({packet_id}, {param_id}, {param_val}, '{ts}', {g})" for param_id, param_val in request.measures)


class AddMobileMeasureResponseBuilder(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules for
    translating a set of *AddMobileMeasureRequest* items into
    an *AddMobileMeasureResponse* Generator.
    """

    def __init__(
            self,
            requests: IterableItemsABC,         # The class that holds the requests items.
            start_packet_id: int                # The database id from where to start counting the measure packets.
    ):
        self.requests = requests
        self.start_packet_id = start_packet_id

    def items(self) -> Generator[AddMobileMeasureResponse, None, None]:
        packet_id_counter = count(self.start_packet_id)
        for req in self.requests:
            yield AddMobileMeasureResponse(
                measure_record=mobile_measure_record(packet_id=next(packet_id_counter), request=req)
            )


def station_measure_record(packet_id: int, sensor_id: int, request: AddSensorMeasuresRequest) -> str:
    ts = request.timestamp
    return ','.join(
        f"({packet_id}, {sensor_id}, {param_id}, {param_val}, '{ts}')" for
        param_id, param_val in request.measures
    )


class AddStationMeasuresResponseBuilder(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules for
    translating a set of *AddSensorMeasuresRequest* items into
    an *AddStationMeasuresResponse* generator.
    """

    def __init__(
            self,
            requests: IterableItemsABC,         # The class that holds the requests items.
            start_packet_id: int,               # The database id from where to start counting the measure packets.
            sensor_id: int                      # The sensor's database id from which the data derives from.
    ):
        self.requests = requests
        self.start_packet_id = start_packet_id
        self.sensor_id = sensor_id

    def items(self) -> Generator[AddStationMeasuresResponse, None, None]:
        packet_id_counter = count(self.start_packet_id)
        for req in self.requests:
            yield AddStationMeasuresResponse(
                measure_record=station_measure_record(
                    packet_id=next(packet_id_counter),
                    sensor_id=self.sensor_id,
                    request=req
                )
            )


class AddPlacesResponseBuilder(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules for
    translating a set of *AddPlacesRequests* items into
    an *AddPlacesResponse* generator.
    """

    def __init__(self, requests: IterableItemsABC):
        self.requests = requests

    def items(self):
        for req in self.requests:
            yield AddPlacesResponse(
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


class AddOpenWeatherMapDataResponseBuilder(IterableItemsABC):

    DAILY_ATTRIBUTES = ['weather_id', 'temperature', 'min_temp', 'max_temp', 'pressure', 'humidity', 'wind_speed', 'wind_direction', 'rain', 'pop', 'snow', 'timestamp']
    HOURLY_ATTRIBUTES = ['weather_id', 'temperature', 'pressure', 'humidity', 'wind_speed', 'wind_direction', 'rain', 'pop', 'snow', 'timestamp']
    CURRENT_ATTRIBUTES = ['weather_id', 'temperature', 'pressure', 'humidity', 'wind_speed', 'wind_direction', 'rain', 'snow', 'timestamp', 'sunrise', 'sunset']
    ALERT_ATTRIBUTES = ['sender_name', 'alert_event', 'alert_begin', 'alert_until', 'description']

    def __init__(
            self,
            requests: IterableItemsABC,
            geoarea_id: int
    ):
        self.requests = requests
        self.geoarea_id = geoarea_id

    def items(self) -> Generator[AddOpenWeatherMapDataResponse, None, None]:
        for req in self.requests:
            yield AddOpenWeatherMapDataResponse(
                current_weather_record=self._record_of(body=_body_of(source=req.current, attributes=self.CURRENT_ATTRIBUTES)),
                hourly_forecast_record=','.join(self._record_of(body=_body_of(source=item, attributes=self.HOURLY_ATTRIBUTES)) for item in req.hourly),
                daily_forecast_record=','.join(self._record_of(body=_body_of(source=item, attributes=self.DAILY_ATTRIBUTES)) for item in req.daily),
                weather_alert_record=','.join(self._record_of(body=_body_of(source=item, attributes=self.ALERT_ATTRIBUTES)) for item in req.alerts)
            )

    def _record_of(self, body: str) -> str:
        return self._header_of() + body + ')'

    def _header_of(self):
        return f"({self.geoarea_id}, "
