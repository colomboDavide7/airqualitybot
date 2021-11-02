#################################################
#
# @Author: davidecolombo
# @Date: mar, 26-10-2021, 12:00
# @Description: this script defines the classes for reshaping a packet before passing it to the SQLQueryBuilder and
#               insert data into the database
#
#################################################
import builtins
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from airquality.parser.datetime_parser import DatetimeParser
from airquality.geom.postgis_geometry import PostGISPointFactory
from airquality.api2database.measurement_packet import MobileMeasurementPacket

from airquality.constants.shared_constants import EMPTY_LIST, EMPTY_DICT, \
    ATMOTUBE_TIME_PARAM, ATMOTUBE_COORDS_PARAM


class Dict2MobilepacketReshaper(ABC):

    @abstractmethod
    def reshape_packets(self, packets: List[Dict[str, Any]], reshape_mapping: Dict[str, Any]) -> List[MobileMeasurementPacket]:
        pass


class Dict2MobilepacketReshaperAtmotube(Dict2MobilepacketReshaper):

    def reshape_packets(self, packets: List[Dict[str, Any]], reshape_mapping: Dict[str, Any]) -> List[MobileMeasurementPacket]:

        reshaped_packets = []
        if packets == EMPTY_LIST:
            return reshaped_packets

        if reshape_mapping == EMPTY_DICT:
            raise SystemExit(f"{Dict2MobilepacketReshaperAtmotube.__name__}: cannot reshape packets when reshape mapping"
                             f" is empty.")

        for packet in packets:
            timestamp = DatetimeParser.atmotube_to_sqltimestamp(packet[ATMOTUBE_TIME_PARAM])
            geom = "null"
            if ATMOTUBE_COORDS_PARAM in packet.keys():
                point = PostGISPointFactory(lat=packet[ATMOTUBE_COORDS_PARAM]["lat"],
                                            lng=packet[ATMOTUBE_COORDS_PARAM]["lon"]).create_geometry()
                geom = point.get_database_string()

            for name, val in packet.items():
                if name in reshape_mapping.keys():
                    reshaped_packets.append(MobileMeasurementPacket(param_id=reshape_mapping[name],
                                                                    param_val=val,
                                                                    timestamp=timestamp,
                                                                    geom=geom))
        return reshaped_packets


################################ FACTORY ################################
class Dict2MobilepacketReshaperFactory(builtins.object):

    @classmethod
    def create_api2database_reshaper(cls, bot_personality: str) -> Dict2MobilepacketReshaper:

        if bot_personality == "atmotube":
            return Dict2MobilepacketReshaperAtmotube()
        else:
            raise SystemExit(
                f"{Dict2MobilepacketReshaperFactory.__name__}: cannot instantiate {Dict2MobilepacketReshaper.__name__} "
                f"instance for personality='{bot_personality}'.")
