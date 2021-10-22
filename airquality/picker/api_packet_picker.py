#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 11:47
# @Description: this script defines the classes for picking sensor's API packet values
#
#################################################
import builtins
from typing import Dict, Any, List
from airquality.parser.datetime_parser import DatetimeParser
from airquality.geom.postgis_geom_builder import PostGISGeomBuilder


class APIPacketPicket(builtins.object):

    """This parameter are defined within the APIPacketPicker class and are used for building the output
    dictionary from the methods. The SQLQueryBuilder will use this variables to unpack the dictionary and
    create a query from it."""


    PARAM_ID  = "par_id"
    SENSOR_ID = "sens_id"
    PARAM_VALUE = "par_val"
    TIMESTAMP = "ts"
    GEOMETRY = "geom"


    @staticmethod
    def pick_atmotube_api_packet(parsed_api_answer: List[Dict[str, Any]], param_id_code: Dict[str, int]) -> List[Dict[str, Any]]:
        """Static method that returns a list of dictionaries. Each dictionary contains the key-value for inserting
        measurement into the database.

        -key:   identifier for the database table attribute (one of the class variable defines in this class)
        -value: value measured by the sensor."""

        outcome = []

        for packet in parsed_api_answer:
            timestamp = DatetimeParser.parser_atmotube_timestamp(packet["time"])
            geom = "null"
            if packet.get("coords", None) is not None:
                geom = PostGISGeomBuilder.build_ST_Point_from_coords(x = packet["coords"]["lon"], y = packet["coords"]["lat"])

            for name, val in packet.items():
                if name in param_id_code.keys():
                    outcome.append({APIPacketPicket.PARAM_ID: param_id_code[name],
                                    APIPacketPicket.PARAM_VALUE: f"'{val}'",
                                    APIPacketPicket.TIMESTAMP: f"'{timestamp}'",
                                    APIPacketPicket.GEOMETRY: geom})
        return outcome
