######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 17:16
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from abc import ABC
from airquality.packet.sql_wrapper_packet import SQLWrapperPacket
from airquality.packet.plain_api_packet import PlainAPIPacketPurpleair


class SQLWrapperSensorPacket(SQLWrapperPacket, ABC):
    pass


class SQLWrapperSensorPacketPurpleair(SQLWrapperSensorPacket):

    def __init__(self, packet: PlainAPIPacketPurpleair):
        self.packet = packet

    def sql(self) -> str:
        return f"('purpleair', '{self.packet.purpleair_identifier}')"

    def __str__(self):
        return f"sensor_name={self.packet.purpleair_identifier}"
