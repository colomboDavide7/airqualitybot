######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 04/11/21 18:52
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from abc import ABC, abstractmethod
from typing import Dict, Any
from airquality.plain.plain_api_packet_mergeable import PlainAPIPacketMergeable
from airquality.sqlwrapper.sql_wrapper_station_packet import SQLWrapperStationPacket, \
    SQLWrapperStationPacketThingspeak1A, SQLWrapperStationPacketThingspeak1B, \
    SQLWrapperStationPacketThingspeak2A, SQLWrapperStationPacketThingspeak2B


class SQLWrapperStationPacketFactory(ABC):

    @abstractmethod
    def create_station_sqlwrapper(self, mapping: Dict[str, Any], sensor_id: int, packet: PlainAPIPacketMergeable
                                  ) -> SQLWrapperStationPacket:
        pass


class SQLWrapperStationPacketThingspeak1AFactory(SQLWrapperStationPacketFactory):

    def create_station_sqlwrapper(self, mapping: Dict[str, Any], sensor_id: int, packet: PlainAPIPacketMergeable
                                  ) -> SQLWrapperStationPacket:
        return SQLWrapperStationPacketThingspeak1A(mapping=mapping, sensor_id=sensor_id, packet=packet)


class SQLWrapperStationPacketThingspeak1BFactory(SQLWrapperStationPacketFactory):

    def create_station_sqlwrapper(self, mapping: Dict[str, Any], sensor_id: int, packet: PlainAPIPacketMergeable
                                  ) -> SQLWrapperStationPacket:
        return SQLWrapperStationPacketThingspeak1B(mapping=mapping, sensor_id=sensor_id, packet=packet)


class SQLWrapperStationPacketThingspeak2AFactory(SQLWrapperStationPacketFactory):

    def create_station_sqlwrapper(self, mapping: Dict[str, Any], sensor_id: int, packet: PlainAPIPacketMergeable
                                  ) -> SQLWrapperStationPacket:
        return SQLWrapperStationPacketThingspeak2A(mapping=mapping, sensor_id=sensor_id, packet=packet)


class SQLWrapperStationPacketThingspeak2BFactory(SQLWrapperStationPacketFactory):

    def create_station_sqlwrapper(self, mapping: Dict[str, Any], sensor_id: int, packet: PlainAPIPacketMergeable
                                  ) -> SQLWrapperStationPacket:
        return SQLWrapperStationPacketThingspeak2B(mapping=mapping, sensor_id=sensor_id, packet=packet)
