######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 03/11/21 19:56
# Description:
#
######################################################

from abc import ABC
from typing import Dict, Any
from airquality.sqlwrapper.sql_wrapper_packet import SQLWrapperPacket
from airquality.plain.plain_api_packet import PlainAPIPacketAtmotube

DEFAULT_VALUE = 'null'


class SQLWrapperMobilePacket(SQLWrapperPacket, ABC):

    def __init__(self, mapping: Dict[str, Any]):
        self.mapping = mapping


class SQLWrapperMobilePacketAtmotube(SQLWrapperMobilePacket):

    def __init__(self, mapping: Dict[str, Any], packet: PlainAPIPacketAtmotube):
        super().__init__(mapping)
        self.packet = packet
        self.voc_param_id = self.mapping.get('voc', DEFAULT_VALUE)
        self.pm1_param_id = self.mapping.get('pm1', DEFAULT_VALUE)
        self.pm25_param_id = self.mapping.get('pm25', DEFAULT_VALUE)
        self.pm10_param_id = self.mapping.get('pm10', DEFAULT_VALUE)

        # # transform geolocation into valid postGIS data type (if any)
        # self.geom = DEFAULT_VALUE
        # if self.packet.latitude != DEFAULT_VALUE and self.packet.longitude != DEFAULT_VALUE:
        #     tmp = PostGISPointFactory(lat=self.packet.latitude, lng=self.packet.longitude).create_geometry()
        #     self.geom = tmp.get_database_string()

    def sql(self) -> str:
        query = ""
        query += f"({self.voc_param_id}, '{self.packet.voc}', '{self.packet.time}', {self.geom}),"
        query += f"({self.pm1_param_id}, '{self.packet.pm1}', '{self.packet.time}', {self.geom}),"
        query += f"({self.pm25_param_id}, '{self.packet.pm25}', '{self.packet.time}', {self.geom}),"
        query += f"({self.pm10_param_id}, '{self.packet.pm10}', '{self.packet.time}', {self.geom})"
        return query

    def __str__(self):
        return f"voc_param_id={self.voc_param_id}, voc={self.packet.voc}, " \
               f"pm1.0_param_id={self.pm1_param_id}, pm1.0={self.packet.pm1}, " \
               f"pm2.5_param_id={self.pm25_param_id}, pm2.5={self.packet.pm25}, " \
               f"pm10.0_param_id={self.pm10_param_id}, pm10.0={self.packet.pm10}, " \
               f"time={self.packet.time}, geom={self.geom}"
