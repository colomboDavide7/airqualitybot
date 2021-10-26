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
from airquality.constants.shared_constants import EMPTY_LIST, \
    ATMOTUBE_TIME_PARAM, ATMOTUBE_COORDS_PARAM, \
    GEO_TYPE_ST_POINT_2D, GEOMBUILDER_LATITUDE, GEOMBUILDER_LONGITUDE, \
    PICKER2SQLBUILDER_PARAM_ID, PICKER2SQLBUILDER_PARAM_VAL, PICKER2SQLBUILDER_TIMESTAMP, PICKER2SQLBUILDER_GEOMETRY


class API2DatabaseReshaper(ABC):


    @abstractmethod
    def reshape_packets(self, packets: Dict[str, Any], measure_param_map: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass


class API2DatabaseReshaperAtmotube(API2DatabaseReshaper):


    def reshape_packets(self, packets: Dict[str, Any], measure_param_map: Dict[str, Any]) -> List[Dict[str, Any]]:

        packets = packets["data"]["items"]

        outcome = []
        if packets == EMPTY_LIST:
            return outcome

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
                    outcome.append({PICKER2SQLBUILDER_PARAM_ID: measure_param_map[name],
                                    PICKER2SQLBUILDER_PARAM_VAL: f"'{val}'",
                                    PICKER2SQLBUILDER_TIMESTAMP: f"'{timestamp}'",
                                    PICKER2SQLBUILDER_GEOMETRY: geom})
        return outcome



class API2DatabaseReshaperFactory(builtins.object):


    @classmethod
    def create_api2database_reshaper(cls, bot_personality: str) -> API2DatabaseReshaper:

        if bot_personality == "atmotube":
            return API2DatabaseReshaperAtmotube()
        else:
            raise SystemExit(f"{API2DatabaseReshaperFactory.__name__}: invalid personality '{bot_personality}'.")
