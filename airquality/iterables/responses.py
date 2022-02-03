######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 18:54
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from itertools import count
from typing import Generator
from airquality.extra.sqlize import sqlize_obj
from airquality.iterables.abc import IterableItemsABC
from airquality.datamodel.fromdb import SensorApiParamDM
from airquality.datamodel.responses import AddFixedSensorResponse, AddSensorMeasureResponse, \
    AddPlaceResponse, AddWeatherDataResponse


class FixedSensorIterableResponses(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and defines the business rules for converting
    an *AddFixedSensorRequest* object into *AddFixedSensorResponse* object.
    """

    SENSOR_ATTRIBUTES = ['type', 'name']
    APIPARAM_ATTRIBUTES = ['api_key', 'api_id', 'channel_name', 'last_acquisition']

    def __init__(self, start_sensor_id: int, requests: IterableItemsABC):
        self._requests = requests
        self._start_sensor_id = start_sensor_id

    def items(self) -> Generator[AddFixedSensorResponse, None, None]:
        sensor_id_counter = count(self._start_sensor_id)
        for req in self._requests:
            hdr = str(next(sensor_id_counter))
            yield AddFixedSensorResponse(
                sensor_record=sqlize_obj(self=req, attributes=self.SENSOR_ATTRIBUTES, header=hdr),
                apiparam_record=','.join(sqlize_obj(self=ch, attributes=self.APIPARAM_ATTRIBUTES, header=hdr)
                                         for ch in req.channel_param)
            )

    def query(self) -> str:
        sensor = param = ""
        for item in self.items():
            sensor += item.sensor_record+','
            param += item.apiparam_record+','
        return f"INSERT INTO level0_raw.sensor VALUES {sensor.strip(',')};" \
               "INSERT INTO level0_raw.sensor_api_param (sensor_id, ch_key, ch_id, ch_name, last_acquisition) " \
               f"VALUES {param.strip(',')};"


class MobileMeasureIterableResponses(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and defines the business rules for converting
    an *AddSensorMeasureRequest* object into *AddSensorMeasureResponse* object for mobile sensors.
    """

    def __init__(self, start_packet_id: int, requests: IterableItemsABC, sensor_param: SensorApiParamDM):
        self.requests = requests
        self._sensor_param = sensor_param
        self.start_packet_id = start_packet_id

    def items(self) -> Generator[AddSensorMeasureResponse, None, None]:
        packet_id_counter = count(self.start_packet_id)
        for req in self.requests:
            packet_id = next(packet_id_counter)
            yield AddSensorMeasureResponse(
                measure_record=','.join(f"({packet_id}, {param_id}, {param_val}, '{req.timestamp}', {req.geolocation})"
                                        for param_id, param_val in req.measures)
            )

    def query(self) -> str:
        query = "INSERT INTO level0_raw.mobile_measurement " \
           "(packet_id, param_id, param_value, timestamp, geom) " \
           f"VALUES {','.join(item.measure_record for item in self.items())};"
        query += "UPDATE level0_raw.sensor_api_param " \
           f"SET last_acquisition = '{self.requests[-1].timestamp}' " \
           f"WHERE sensor_id = {self._sensor_param.sensor_id} AND ch_name = '{self._sensor_param.ch_name}';"
        return query


class StationMeasureIterableResponses(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and defines the business rules for converting
    an *AddSensorMeasureRequest* object into *AddSensorMeasureResponse* object for fixed sensors.
    """

    def __init__(self, sensor_param: SensorApiParamDM, start_packet_id: int, requests: IterableItemsABC):
        self._requests = requests
        self._sensor_param = sensor_param
        self._start_packet_id = start_packet_id

    def items(self) -> Generator:
        packet_id_counter = count(self._start_packet_id)
        for req in self._requests:
            packet_id  = next(packet_id_counter)
            yield AddSensorMeasureResponse(
                measure_record=','.join(f"({packet_id}, {self._sensor_param.sensor_id}, {param_id}, {param_val}, "
                                        f"'{req.timestamp}')" for param_id, param_val in req.measures)
            )

    def query(self) -> str:
        query = "INSERT INTO level0_raw.station_measurement " \
           "(packet_id, sensor_id, param_id, param_value, timestamp) " \
           f"VALUES {','.join(item.measure_record for item in self.items())};"
        query += "UPDATE level0_raw.sensor_api_param " \
           f"SET last_acquisition = '{self._requests[-1].timestamp}' " \
           f"WHERE sensor_id = {self._sensor_param.sensor_id} AND ch_name = '{self._sensor_param.ch_name}';"
        return query


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
                place_record=f"('{req.poscode}', '{req.countrycode}', '{req.placename}', "
                             f"'{req.province}', '{req.state}', {req.geolocation})"
            )


class WeatherDataIterableResponses(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and defines the business rules for converting
    an *AddWeatherDataRequest* object into *AddWeatherDataResponse* object for fixed sensors.
    """

    DAILY_ATTRIBUTES = ['weather_id', 'temperature', 'min_temp', 'max_temp', 'pressure', 'humidity', 'wind_speed', 'wind_direction', 'rain', 'pop', 'snow', 'timestamp']
    HOURLY_ATTRIBUTES = ['weather_id', 'temperature', 'pressure', 'humidity', 'wind_speed', 'wind_direction', 'rain', 'pop', 'snow', 'timestamp']
    CURRENT_ATTRIBUTES = ['weather_id', 'temperature', 'pressure', 'humidity', 'wind_speed', 'wind_direction', 'rain', 'snow', 'timestamp', 'sunrise', 'sunset']
    ALERT_ATTRIBUTES = ['sender_name', 'alert_event', 'alert_begin', 'alert_until', 'description']

    def __init__(self, geoarea_id: int, requests: IterableItemsABC):
        self.requests = requests
        self.geoarea_id = geoarea_id

    def items(self) -> Generator:
        for req in self.requests:
            hdr = str(self.geoarea_id)
            yield AddWeatherDataResponse(
                current_weather_record=sqlize_obj(self=req.current, attributes=self.CURRENT_ATTRIBUTES, header=hdr),
                hourly_forecast_record=','.join(sqlize_obj(self=item, attributes=self.HOURLY_ATTRIBUTES, header=hdr) for item in req.hourly),
                daily_forecast_record=','.join(sqlize_obj(self=item, attributes=self.DAILY_ATTRIBUTES, header=hdr) for item in req.daily),
                weather_alert_record=','.join(sqlize_obj(self=item, attributes=self.ALERT_ATTRIBUTES, header=hdr) for item in req.alerts)
            )
