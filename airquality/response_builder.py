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
from airquality.response import AddFixedSensorResponse, AddMobileMeasureResponse

SQL_TIMESTAMP_FTM = "%Y-%m-%d %H:%M:%S"
POSTGIS_POINT = "POINT({lon} {lat})"
ST_GEOM_FROM_TEXT = "ST_GeomFromText('{geom}', {srid})"


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
        sensor_id = count(self.start_sensor_id)
        for req in self.requests:
            sid = next(sensor_id)
            sensor_record = f"({sid}, '{req.type}', '{req.name}')"
            apiparam_record = ','.join(
                f"({sid}, '{ch.api_key}', '{ch.api_id}', '{ch.channel_name}', '{ch.last_acquisition}')" for ch in req.channels
            )

            valid_from = datetime.now().strftime(SQL_TIMESTAMP_FTM)
            geom = req.geolocation.geometry_as_text
            geolocation_record = f"({sid}, '{valid_from}', {geom})"

            yield AddFixedSensorResponse(
                sensor_record=sensor_record, apiparam_record=apiparam_record, geolocation_record=geolocation_record
            )


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
            timestamp = req.timestamp.strftime(SQL_TIMESTAMP_FTM)
            geometry = req.geolocation.geometry_as_text

            packet_id = next(packet_id_counter)
            measure_record = ','.join(
                f"({packet_id}, {param_id}, '{param_val}', '{timestamp}', {geometry})" for param_id, param_val in req.measures
            )

            yield AddMobileMeasureResponse(measure_record=measure_record)
