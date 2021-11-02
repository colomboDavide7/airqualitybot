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
from airquality.geom.postgis_geom_builder import PostGISGeomBuilder
from airquality.api2database.measurement_packet import MobileMeasurementPacket
from airquality.constants.shared_constants import EMPTY_LIST, EMPTY_DICT, \
    ATMOTUBE_TIME_PARAM, ATMOTUBE_COORDS_PARAM, \
    GEO_TYPE_ST_POINT_2D, GEOMBUILDER_LATITUDE, GEOMBUILDER_LONGITUDE, \
    PURPLEAIR_LAT_PARAM, PURPLEAIR_LON_PARAM, PURPLEAIR_SENSOR_IDX_PARAM, PURPLEAIR_NAME_PARAM


class API2DatabaseReshaper(ABC):

    @abstractmethod
    def reshape_packets(self, packets: List[Dict[str, Any]], reshape_mapping: Dict[str, Any]) -> List[MobileMeasurementPacket]:
        pass


class API2DatabaseReshaperAtmotube(API2DatabaseReshaper):

    def reshape_packets(self, packets: List[Dict[str, Any]], reshape_mapping: Dict[str, Any]) -> List[MobileMeasurementPacket]:

        reshaped_packets = []
        if packets == EMPTY_LIST:
            return reshaped_packets

        if reshape_mapping == EMPTY_DICT:
            raise SystemExit(f"{API2DatabaseReshaperAtmotube.__name__}: cannot reshape packets when reshape mapping is "
                             f"empty.")

        for packet in packets:
            timestamp = DatetimeParser.atmotube_to_sqltimestamp(packet[ATMOTUBE_TIME_PARAM])
            geom = "null"
            if ATMOTUBE_COORDS_PARAM in packet.keys():
                geom = PostGISGeomBuilder.build_geometry_type(
                    geo_param={GEOMBUILDER_LONGITUDE: packet[ATMOTUBE_COORDS_PARAM]["lon"],
                               GEOMBUILDER_LATITUDE: packet[ATMOTUBE_COORDS_PARAM]["lat"]},
                    geo_type=GEO_TYPE_ST_POINT_2D)

            for name, val in packet.items():
                if name in reshape_mapping.keys():
                    reshaped_packets.append(MobileMeasurementPacket(param_id=reshape_mapping[name],
                                                                    param_val=val,
                                                                    timestamp=timestamp,
                                                                    geom=geom))
        return reshaped_packets


class API2DatabaseReshaperPurpleair(API2DatabaseReshaper):

    def reshape_packets(self, packets: List[Dict[str, Any]], reshape_mapping: Dict[str, Any]) -> List[Dict[str, Any]]:

        if packets == EMPTY_LIST:
            return []

        if reshape_mapping == EMPTY_DICT:
            raise SystemExit(
                f"{API2DatabaseReshaperPurpleair.__name__}: cannot reshape packets when reshape mapping is "
                f"empty.")

        reshaped_packets = []
        for packet in packets:
            # GET THE PACKET KEYS TO AVOID CALLING THE METHOD MULTIPLE TIMES
            keys = packet.keys()

            # CHECK IF THERE ARE LATITUDE AND LONGITUDE INSIDE THE PACKET
            if PURPLEAIR_LAT_PARAM not in keys or PURPLEAIR_LON_PARAM not in keys:
                raise SystemExit(f"{API2DatabaseReshaperPurpleair.__name__}: missing purpleair geolocation parameters.")
            geom = PostGISGeomBuilder.build_geometry_type(geo_param={GEOMBUILDER_LONGITUDE: packet[PURPLEAIR_LON_PARAM],
                                                                     GEOMBUILDER_LATITUDE: packet[PURPLEAIR_LAT_PARAM]},
                                                          geo_type=GEO_TYPE_ST_POINT_2D)

            # CHECK IF SENSOR NAME PARAMETERS ARE MISSING OR NOT
            if PURPLEAIR_NAME_PARAM not in keys or PURPLEAIR_SENSOR_IDX_PARAM not in keys:
                raise SystemExit(f"{API2DatabaseReshaperPurpleair.__name__}: missing purpleair name parameters.")
            sensor_name = f"{packet[PURPLEAIR_NAME_PARAM]} ({packet[PURPLEAIR_SENSOR_IDX_PARAM]})"

            # USE THE RESHAPER MAPPING TO RESHAPE THE PACKETS
            if sensor_name in reshape_mapping.keys():
                reshaped_packets.append({reshape_mapping[sensor_name]: geom})

        return reshaped_packets


################################ FACTORY ################################
class API2DatabaseReshaperFactory(builtins.object):

    @classmethod
    def create_api2database_reshaper(cls, bot_personality: str) -> API2DatabaseReshaper:

        if bot_personality == "atmotube":
            return API2DatabaseReshaperAtmotube()
        elif bot_personality == "purpleair":
            return API2DatabaseReshaperPurpleair()
        else:
            raise SystemExit(
                f"{API2DatabaseReshaperFactory.__name__}: cannot instantiate {API2DatabaseReshaper.__name__} "
                f"instance for personality='{bot_personality}'.")
