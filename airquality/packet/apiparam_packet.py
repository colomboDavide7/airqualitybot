######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 16:13
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from abc import ABC
from airquality.packet.packet import Packet
from airquality.packet.apiparam_single_packet import APIParamSinglePacketPurpleair


class APIParamPacket(Packet, ABC):

    def __init__(self, sensor_id: int):
        self.sensor_id = sensor_id


class APIParamPacketPurpleair(APIParamPacket):

    def __init__(self, sensor_id: int, packet: APIParamSinglePacketPurpleair):
        super().__init__(sensor_id)
        self.packet = packet

    def sql(self) -> str:
        query = ""
        query += f"({self.sensor_id}, 'primary_id_a', '{self.packet.primary_id_a}'),"
        query += f"({self.sensor_id}, 'primary_key_a', '{self.packet.primary_key_a}'),"
        query += f"({self.sensor_id}, 'primary_timestamp_a', null),"
        query += f"({self.sensor_id}, 'primary_id_b', '{self.packet.primary_id_b}'),"
        query += f"({self.sensor_id}, 'primary_key_b', '{self.packet.primary_key_b}'),"
        query += f"({self.sensor_id}, 'primary_timestamp_b', null),"
        query += f"({self.sensor_id}, 'secondary_id_a', '{self.packet.secondary_id_a}'),"
        query += f"({self.sensor_id}, 'secondary_key_a', '{self.packet.secondary_key_a}'),"
        query += f"({self.sensor_id}, 'secondary_timestamp_a', null),"
        query += f"({self.sensor_id}, 'secondary_id_b', '{self.packet.secondary_id_b}'),"
        query += f"({self.sensor_id}, 'secondary_key_b', '{self.packet.secondary_key_b}'),"
        query += f"({self.sensor_id}, 'secondary_timestamp_b', null)"
        return query

    def __str__(self):
        return f"primary_id_a={self.packet.primary_id_a}, primary_key_a={self.packet.primary_key_a}, " \
               f"primary_id_b={self.packet.primary_id_b}, primary_key_b={self.packet.primary_key_b}, " \
               f"secondary_id_a={self.packet.secondary_id_a}, secondary_key_a={self.packet.secondary_key_a}, " \
               f"secondary_id_b={self.packet.secondary_id_b}, secondary_key_b={self.packet.secondary_key_b}, " \
               f"primary_timestamp_a=null, primary_timestamp_b=null, secondary_timestamp_a=null, " \
               f"secondary_timestamp_b=null"
