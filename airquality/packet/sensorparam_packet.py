######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 17:16
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from abc import ABC
from airquality.packet.packet import Packet
from airquality.packet.apiparam_single_packet import APIParamSinglePacketPurpleair


class SensorParamPacket(Packet, ABC):
    pass


class SensorParamPacketPurpleair(SensorParamPacket):

    def __init__(self, packet: APIParamSinglePacketPurpleair):
        self.packet = packet

    def sql(self) -> str:
        return f"('purpleair', '{self.packet.purpleair_identifier}')"

    def __str__(self):
        return f"sensor_name={self.packet.purpleair_identifier}"
