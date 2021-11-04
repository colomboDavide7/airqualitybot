######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 04/11/21 18:26
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import builtins
from typing import List, Dict, Any
from abc import ABC, abstractmethod
from airquality.sqlwrapper.sql_wrapper_packet import SQLWrapperPacket
from airquality.plain.plain_api_packet_mergeable import PlainAPIPacketThingspeakPrimaryChannelA,\
    PlainAPIPacketThingspeakPrimaryChannelB, PlainAPIPacketThingspeakSecondaryChannelA, \
    PlainAPIPacketThingspeakSecondaryChannelB

from airquality.sqlwrapper.sql_wrapper_station_packet_factory import SQLWrapperStationPacketThingspeak1AFactory, \
    SQLWrapperStationPacketThingspeak1BFactory, SQLWrapperStationPacketThingspeak2AFactory, \
    SQLWrapperStationPacketThingspeak2BFactory


class WrapperStationPacket(ABC):

    @abstractmethod
    def decode_packets(self, packets: List[builtins.object]) -> List[SQLWrapperPacket]:
        pass


class WrapperStationPacketThingspeak(WrapperStationPacket):

    def __init__(self, mapping: Dict[str, Any], sensor_id: int):
        self.mapping = mapping
        self.sensor_id = sensor_id

    def decode_packets(self, packets: List[builtins.object]) -> List[SQLWrapperPacket]:

        if not packets:
            return []

        wrapped_packets = []
        if isinstance(packets[0], PlainAPIPacketThingspeakPrimaryChannelA):
            factory = SQLWrapperStationPacketThingspeak1AFactory()
        elif isinstance(packets[0], PlainAPIPacketThingspeakPrimaryChannelB):
            factory = SQLWrapperStationPacketThingspeak1BFactory()
        elif isinstance(packets[0], PlainAPIPacketThingspeakSecondaryChannelA):
            factory = SQLWrapperStationPacketThingspeak2AFactory()
        elif isinstance(packets[0], PlainAPIPacketThingspeakSecondaryChannelB):
            factory = SQLWrapperStationPacketThingspeak2BFactory()
        else:
            raise SystemExit(f"{WrapperStationPacketThingspeak.__name__}: cannot instantiate a factory for "
                             f"'{SQLWrapperPacket.__name__}")

        for packet in packets:
            wrapped_packets.append(
                factory.create_station_sqlwrapper(
                    mapping=self.mapping, sensor_id=self.sensor_id, packet=packet
                )
            )

        return wrapped_packets


class WrapperStationPacketFactory(builtins.object):

    @classmethod
    def create_packet_wrapper(cls, bot_personality: str, mapping: Dict[str, Any], sensor_id: int) -> WrapperStationPacket:
        if bot_personality == "thingspeak":
            return WrapperStationPacketThingspeak(mapping=mapping, sensor_id=sensor_id)
        else:
            raise SystemExit(f"{WrapperStationPacketFactory.__name__}: cannot instantiate {WrapperStationPacket.__name__} "
                             f"instance for personality='{bot_personality}'.")
