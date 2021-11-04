######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 04/11/21 12:42
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from abc import ABC
from typing import Dict, Any
from airquality.sqlwrapper.sql_wrapper_packet import SQLWrapperPacket
from airquality.plain.plain_api_packet_mergeable import PlainAPIPacketThingspeakPrimaryChannelA, \
    PlainAPIPacketThingspeakPrimaryChannelB, PlainAPIPacketThingspeakSecondaryChannelA, \
    PlainAPIPacketThingspeakSecondaryChannelB


class SQLWrapperStationPacket(SQLWrapperPacket, ABC):

    def __init__(self, mapping: Dict[str, Any], sensor_id: int):
        self.mapping = mapping
        self.sensor_id = sensor_id


class SQLWrapperStationPacketThingspeak1A(SQLWrapperStationPacket):

    def __init__(self, mapping: Dict[str, Any], sensor_id: int, packet: PlainAPIPacketThingspeakPrimaryChannelA):
        super().__init__(mapping, sensor_id)
        self.packet = packet
        self.pm1_param_id = self.mapping.get('pm1.0_atm_a')
        self.pm25_param_id = self.mapping.get('pm2.5_atm_a')
        self.pm10_param_id = self.mapping.get('pm10.0_atm_a')
        self.temp_param_id = self.mapping.get('temperature_a')
        self.hum_param_id = self.mapping.get('humidity_a')

    def sql(self) -> str:
        query = ""
        query += f"({self.pm1_param_id}, {self.sensor_id}, '{self.packet.pm1}', '{self.packet.created_at}'),"
        query += f"({self.pm25_param_id}, {self.sensor_id}, '{self.packet.pm25}', '{self.packet.created_at}'),"
        query += f"({self.pm10_param_id}, {self.sensor_id}, '{self.packet.pm10}', '{self.packet.created_at}'),"
        query += f"({self.temp_param_id}, {self.sensor_id}, '{self.packet.temperature}', '{self.packet.created_at}'),"
        query += f"({self.hum_param_id}, {self.sensor_id}, '{self.packet.humidity}', '{self.packet.created_at}')"
        return query

    def __str__(self):
        return f"pm1.0_param_id={self.pm1_param_id}, pm1.0={self.packet.pm1}, " \
               f"pm2.5_param_id={self.pm25_param_id}, pm2.5={self.packet.pm25}, " \
               f"pm10.0_param_id={self.pm10_param_id}, pm10.0={self.packet.pm10}, " \
               f"temp_param_id={self.temp_param_id}, temperature={self.packet.temperature}, " \
               f"hum_param_id={self.hum_param_id}, humidity={self.packet.humidity}, " \
               f"created_at={self.packet.created_at}"


class SQLWrapperStationPacketThingspeak1B(SQLWrapperStationPacket):

    def __init__(self, mapping: Dict[str, Any], sensor_id: int, packet: PlainAPIPacketThingspeakPrimaryChannelB):
        super().__init__(mapping, sensor_id)
        self.packet = packet
        self.pm1_param_id = self.mapping.get('pm1.0_atm_b')
        self.pm25_param_id = self.mapping.get('pm2.5_atm_b')
        self.pm10_param_id = self.mapping.get('pm10.0_atm_b')
        self.pres_param_id = self.mapping.get('pressure_b')

    def sql(self) -> str:
        query = ""
        query += f"({self.pm1_param_id}, {self.sensor_id}, '{self.packet.pm1}', '{self.packet.created_at}'),"
        query += f"({self.pm25_param_id}, {self.sensor_id}, '{self.packet.pm25}', '{self.packet.created_at}'),"
        query += f"({self.pm10_param_id}, {self.sensor_id}, '{self.packet.pm10}', '{self.packet.created_at}'),"
        query += f"({self.pres_param_id}, {self.sensor_id}, '{self.packet.pressure}', '{self.packet.created_at}')"
        return query

    def __str__(self):
        return f"pm1.0_param_id={self.pm1_param_id}, pm1.0={self.packet.pm1}, " \
               f"pm2.5_param_id={self.pm25_param_id}, pm2.5={self.packet.pm25}, " \
               f"pm10.0_param_id={self.pm10_param_id}, pm10.0={self.packet.pm10}, " \
               f"pres_param_id={self.pres_param_id}, pressure={self.packet.pressure}, " \
               f"created_at={self.packet.created_at}"


class SQLWrapperStationPacketThingspeak2A(SQLWrapperStationPacket):

    def __init__(self, mapping: Dict[str, Any], sensor_id: int, packet: PlainAPIPacketThingspeakSecondaryChannelA):
        super().__init__(mapping, sensor_id)
        self.packet = packet
        self.c_03_param_id = self.mapping.get('0.3_um_count_a')
        self.c_05_param_id = self.mapping.get('0.5_um_count_a')
        self.c_1_param_id = self.mapping.get('1.0_um_count_a')
        self.c_25_param_id = self.mapping.get('2.5_um_count_a')
        self.c_5_param_id = self.mapping.get('5.0_um_count_a')
        self.c_10_param_id = self.mapping.get('10.0_um_count_a')

    def sql(self) -> str:
        query = ""
        query += f"({self.c_03_param_id}, {self.sensor_id}, '{self.packet.count_03}', '{self.packet.created_at}'),"
        query += f"({self.c_05_param_id}, {self.sensor_id}, '{self.packet.count_05}', '{self.packet.created_at}'),"
        query += f"({self.c_1_param_id}, {self.sensor_id}, '{self.packet.count_1}', '{self.packet.created_at}'),"
        query += f"({self.c_25_param_id}, {self.sensor_id}, '{self.packet.count_25}', '{self.packet.created_at}'),"
        query += f"({self.c_5_param_id}, {self.sensor_id}, '{self.packet.count_5}', '{self.packet.created_at}'),"
        query += f"({self.c_10_param_id}, {self.sensor_id}, '{self.packet.count_10}', '{self.packet.created_at}')"
        return query

    def __str__(self):
        return f"c_03_param_id={self.c_03_param_id}, count_0.3={self.packet.count_03}, " \
               f"c_05_param_id={self.c_05_param_id}, count_0.5={self.packet.count_05}, " \
               f"c_1_param_id={self.c_1_param_id}, count_1.0={self.packet.count_1}, " \
               f"c_2.5_param_id={self.c_25_param_id}, count_2.5={self.packet.count_25}, " \
               f"c_5.0_param_id={self.c_5_param_id}, count_5.0={self.packet.count_5}, " \
               f"c_10.0_param_id={self.c_10_param_id}, count_10.0={self.packet.count_10}, " \
               f"created_at={self.packet.created_at}"


class SQLWrapperStationPacketThingspeak2B(SQLWrapperStationPacket):

    def __init__(self, mapping: Dict[str, Any], sensor_id: int, packet: PlainAPIPacketThingspeakSecondaryChannelB):
        super().__init__(mapping, sensor_id)
        self.packet = packet
        self.c_03_param_id = self.mapping.get('0.3_um_count_b')
        self.c_05_param_id = self.mapping.get('0.5_um_count_b')
        self.c_1_param_id = self.mapping.get('1.0_um_count_b')
        self.c_25_param_id = self.mapping.get('2.5_um_count_b')
        self.c_5_param_id = self.mapping.get('5.0_um_count_b')
        self.c_10_param_id = self.mapping.get('10.0_um_count_b')

    def sql(self) -> str:
        query = ""
        query += f"({self.c_03_param_id}, {self.sensor_id}, '{self.packet.count_03}', '{self.packet.created_at}'),"
        query += f"({self.c_05_param_id}, {self.sensor_id}, '{self.packet.count_05}', '{self.packet.created_at}'),"
        query += f"({self.c_1_param_id}, {self.sensor_id}, '{self.packet.count_1}', '{self.packet.created_at}'),"
        query += f"({self.c_25_param_id}, {self.sensor_id}, '{self.packet.count_25}', '{self.packet.created_at}'),"
        query += f"({self.c_5_param_id}, {self.sensor_id}, '{self.packet.count_5}', '{self.packet.created_at}'),"
        query += f"({self.c_10_param_id}, {self.sensor_id}, '{self.packet.count_10}', '{self.packet.created_at}')"
        return query

    def __str__(self):
        return f"c_03_param_id={self.c_03_param_id}, count_0.3={self.packet.count_03}, " \
               f"c_05_param_id={self.c_05_param_id}, count_0.5={self.packet.count_05}, " \
               f"c_1_param_id={self.c_1_param_id}, count_1.0={self.packet.count_1}, " \
               f"c_2.5_param_id={self.c_25_param_id}, count_2.5={self.packet.count_25}, " \
               f"c_5.0_param_id={self.c_5_param_id}, count_5.0={self.packet.count_5}, " \
               f"c_10.0_param_id={self.c_10_param_id}, count_10.0={self.packet.count_10}, " \
               f"created_at={self.packet.created_at}"
