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
                geom = PostGISPointFactory(lat=packet[ATMOTUBE_COORDS_PARAM]["lat"],
                                           lng=packet[ATMOTUBE_COORDS_PARAM]["lon"]).create_geometry()

            for name, val in packet.items():
                if name in reshape_mapping.keys():
                    reshaped_packets.append(MobileMeasurementPacket(param_id=reshape_mapping[name],
                                                                    param_val=val,
                                                                    timestamp=timestamp,
                                                                    geom=geom))
        return reshaped_packets


# class API2DatabaseReshaperPurpleair(Dict2MobilepacketReshaper):
#
#     def reshape_packets(self, packets: List[Dict[str, Any]], reshape_mapping: Dict[str, Any]) -> List[GeoPacket]:
#
#         if packets == EMPTY_LIST:
#             return []
#
#         if reshape_mapping == EMPTY_DICT:
#             raise SystemExit(f"{API2DatabaseReshaperPurpleair.__name__}: cannot reshape packets when reshape mapping "
#                              f"is empty.")
#
#         reshaped_packets = []
#         for packet in packets:
#             # GET THE PACKET KEYS TO AVOID CALLING THE METHOD MULTIPLE TIMES
#             keys = packet.keys()
#
#             # CHECK IF THERE ARE LATITUDE AND LONGITUDE INSIDE THE PACKET
#             if PURPLEAIR_LAT_PARAM not in keys or PURPLEAIR_LON_PARAM not in keys:
#                 raise SystemExit(f"{API2DatabaseReshaperPurpleair.__name__}: missing purpleair geolocation parameters.")
#
#             geom = PostGISGeomBuilder.postgisgeom2geostring(PostGISPoint(lat=packet[PURPLEAIR_LAT_PARAM],
#                                                                          lng=packet[PURPLEAIR_LON_PARAM]))
#
#             # CHECK IF SENSOR NAME PARAMETERS ARE MISSING OR NOT
#             if PURPLEAIR_NAME_PARAM not in keys or PURPLEAIR_SENSOR_IDX_PARAM not in keys:
#                 raise SystemExit(f"{API2DatabaseReshaperPurpleair.__name__}: missing purpleair name parameters.")
#             sensor_name = f"{packet[PURPLEAIR_NAME_PARAM]} ({packet[PURPLEAIR_SENSOR_IDX_PARAM]})"
#
#             if sensor_name in reshape_mapping.keys():
#                 reshaped_packets.append(GeoPacket(sensor_id=reshape_mapping[sensor_name], geom=geom))
#
#         return reshaped_packets


################################ FACTORY ################################
class Dict2MobilepacketReshaperFactory(builtins.object):

    @classmethod
    def create_api2database_reshaper(cls, bot_personality: str) -> Dict2MobilepacketReshaper:

        if bot_personality == "atmotube":
            return Dict2MobilepacketReshaperAtmotube()
        # elif bot_personality == "purpleair":
        #     return API2DatabaseReshaperPurpleair()
        else:
            raise SystemExit(
                f"{Dict2MobilepacketReshaperFactory.__name__}: cannot instantiate {Dict2MobilepacketReshaper.__name__} "
                f"instance for personality='{bot_personality}'.")
