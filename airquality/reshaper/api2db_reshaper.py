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
from airquality.constants.shared_constants import EMPTY_LIST, EMPTY_DICT, \
    ATMOTUBE_TIME_PARAM, ATMOTUBE_COORDS_PARAM, \
    GEO_TYPE_ST_POINT_2D, GEOMBUILDER_LATITUDE, GEOMBUILDER_LONGITUDE, \
    RESHAPER2SQLBUILDER_PARAM_ID, RESHAPER2SQLBUILDER_PARAM_VAL, \
    RESHAPER2SQLBUILDER_TIMESTAMP, RESHAPER2SQLBUILDER_GEOMETRY


class API2DatabaseReshaper(ABC):


    @abstractmethod
    def reshape_packets(self, packets: List[Dict[str, Any]], measure_param_map: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass


class API2DatabaseReshaperAtmotube(API2DatabaseReshaper):


    def reshape_packets(self, packets: List[Dict[str, Any]], measure_param_map: Dict[str, Any]) -> List[Dict[str, Any]]:

        reshaped_packets = []
        if packets == EMPTY_LIST:
            return reshaped_packets

        if measure_param_map == EMPTY_DICT:
            raise SystemExit(f"{API2DatabaseReshaperAtmotube.__name__}: cannot reshape packets when reshape mapping is "
                             f"empty.")

        for packet in packets:
            timestamp = DatetimeParser.atmotube_to_sqltimestamp(packet[ATMOTUBE_TIME_PARAM])
            geom = "null"
            if ATMOTUBE_COORDS_PARAM in packet.keys():
                geom = PostGISGeomBuilder.build_geometry_type(
                        geo_param = {GEOMBUILDER_LONGITUDE: packet[ATMOTUBE_COORDS_PARAM]["lon"],
                                     GEOMBUILDER_LATITUDE: packet[ATMOTUBE_COORDS_PARAM]["lat"]},
                        geo_type = GEO_TYPE_ST_POINT_2D)

            for name, val in packet.items():
                if name in measure_param_map.keys():
                    reshaped_packets.append({RESHAPER2SQLBUILDER_PARAM_ID: measure_param_map[name],
                                             RESHAPER2SQLBUILDER_PARAM_VAL: f"'{val}'",
                                             RESHAPER2SQLBUILDER_TIMESTAMP: f"'{timestamp}'",
                                             RESHAPER2SQLBUILDER_GEOMETRY: geom})
        return reshaped_packets



################################ FACTORY ################################
class API2DatabaseReshaperFactory(builtins.object):


    @classmethod
    def create_api2database_reshaper(cls, bot_personality: str) -> API2DatabaseReshaper:

        if bot_personality == "atmotube":
            return API2DatabaseReshaperAtmotube()
        else:
            raise SystemExit(f"{API2DatabaseReshaperFactory.__name__}: cannot instantiate {API2DatabaseReshaper.__name__} "
                             f"instance for personality='{bot_personality}'.")
