######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 18:54
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from itertools import count
from typing import Generator
from datetime import datetime
from airquality.iteritems import IterableItemsABC
from airquality.request import AddFixedSensorRequest, AddMobileMeasureRequest
from airquality.response import AddFixedSensorResponse, AddMobileMeasureResponse

SQL_TIMESTAMP_FTM = "%Y-%m-%d %H:%M:%S"


def apiparam_record(sensor_id: int, request: AddFixedSensorRequest) -> str:
    return ','.join(
        f"({sensor_id}, '{ch.api_key}', '{ch.api_id}', '{ch.channel_name}', '{ch.last_acquisition}')" for ch in request.channels
    )


def sensor_at_location_record(sensor_id: int, request: AddFixedSensorRequest) -> str:
    valid_from = datetime.now().strftime(SQL_TIMESTAMP_FTM)
    location = request.geolocation.geom_from_text()
    return f"({sensor_id}, '{valid_from}', {location})"


class AddFixedSensorResponseBuilder(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules for
    translating a set of *AddFixedSensorRequest* items into
    an *AddFixedSensorResponse* Generator.
    """

    def __init__(self, requests: IterableItemsABC, start_sensor_id: int):
        self.requests = requests
        self.start_sensor_id = start_sensor_id

    def items(self) -> Generator[AddFixedSensorResponse, None, None]:
        sensor_id_counter = count(self.start_sensor_id)
        for req in self.requests:
            sensor_id = next(sensor_id_counter)
            yield AddFixedSensorResponse(
                sensor_record=f"({sensor_id}, '{req.type}', '{req.name}')",
                apiparam_record=apiparam_record(sensor_id=sensor_id, request=req),
                geolocation_record=sensor_at_location_record(sensor_id=sensor_id, request=req)
            )


def measure_record(packet_id: int, request: AddMobileMeasureRequest) -> str:
    timestamp = request.timestamp.strftime(SQL_TIMESTAMP_FTM)
    geometry = request.geolocation.geom_from_text()
    return ','.join(f"({packet_id}, {param_id}, '{param_val}', '{timestamp}', {geometry})" for param_id, param_val in request.measures)


class AddMobileMeasureResponseBuilder(IterableItemsABC):
    """
        An *IterableItemsABC* that defines the business rules for
        translating a set of *AddMobileMeasureRequest* items into
        an *AddMobileMeasureResponse* Generator.
        """

    def __init__(self, requests: IterableItemsABC, start_packet_id: int):
        self.requests = requests
        self.start_packet_id = start_packet_id

    def items(self) -> Generator[AddMobileMeasureResponse, None, None]:
        packet_id_counter = count(self.start_packet_id)
        for req in self.requests:
            yield AddMobileMeasureResponse(
                measure_record=measure_record(packet_id=next(packet_id_counter), request=req)
            )
