######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 17:35
# Description: this script defines the an Abstract Base Class called GeoParamPacket that extends also Packet class.
#              This classes are used to decode a sqlwrapper coming from API into a string that is used for building the
#              sql query.
#
######################################################

from abc import ABC
from airquality.sqlwrapper.sql_wrapper_packet import SQLWrapperPacket
from airquality.plain.plain_api_packet import PlainAPIPacketPurpleair
from airquality.parser.datetime_parser import DatetimeParser
from airquality.geom.postgis_geometry import PostGISPointFactory


class SQLWrapperGeoPacket(SQLWrapperPacket, ABC):

    def __init__(self, sensor_id: int):
        self.sensor_id = sensor_id


class SQLWrapperGeoPacketPurpleair(SQLWrapperGeoPacket):

    def __init__(self, packet: PlainAPIPacketPurpleair, sensor_id: int):
        super().__init__(sensor_id)
        self.packet = packet
        self.ts = DatetimeParser.current_sqltimestamp()
        self.point = PostGISPointFactory(lat=self.packet.latitude, lng=self.packet.longitude).create_geometry()

    def sql(self) -> str:
        return f"({self.sensor_id}, '{self.ts}', {self.point.get_database_string()})"

    def __str__(self):
        return f"sensor_id={self.sensor_id}, ts={self.ts}, geom={self.point.get_database_string()}"
