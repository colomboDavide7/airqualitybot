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
from airquality.picker import TIMESTAMP, PARAM_VALUE, PARAM_ID, GEOMETRY


class APIPacketPicker(builtins.object):

    """This parameter are defined within the APIPacketPicker class and are used for building the output
    dictionary from the methods. The SQLQueryBuilder will use this variables to unpack the dictionary and
    create a query from it."""


    @staticmethod
    def pick_atmotube_api_packet(parsed_api_answer: List[Dict[str, Any]], param_id_code: Dict[str, int]) -> List[Dict[str, Any]]:
        """Static method that returns a list of dictionaries. Each dictionary contains the key-value for inserting
        measurement into the database.

        -key:   identifier for the database table attribute (one of the class variable defines in this class)
        -value: value measured by the sensor."""

        outcome = []

        for packet in parsed_api_answer:
            timestamp = DatetimeParser.parse_atmotube_timestamp(packet["time"])
            geom = "null"
            if packet.get("coords", None) is not None:
                geom = PostGISGeomBuilder.build_ST_Point_from_coords(x = packet["coords"]["lon"], y = packet["coords"]["lat"])

            for name, val in packet.items():
                if name in param_id_code.keys():
                    outcome.append({PARAM_ID: param_id_code[name],
                                    PARAM_VALUE: f"'{val}'",
                                    TIMESTAMP: f"'{timestamp}'",
                                    GEOMETRY: geom})
        return outcome


    @staticmethod
    def pick_atmotube_api_packets_with_timestamp_offset(
        parsed_api_answer: List[Dict[str, Any]],
        param_id_code: Dict[str, int],
        timestamp_offset: str
    ) -> List[Dict[str, Any]]:

        outcome = []

        for packet in parsed_api_answer:
            timestamp = DatetimeParser.parse_atmotube_timestamp(packet["time"])
            if not DatetimeParser.is_ts1_before_ts2(ts1 = timestamp, ts2 = timestamp_offset):
                geom = "null"
                if packet.get("coords", None) is not None:
                    geom = PostGISGeomBuilder.build_ST_Point_from_coords(x = packet["coords"]["lon"],
                                                                         y = packet["coords"]["lat"])

                for name, val in packet.items():
                    if name in param_id_code.keys():
                        outcome.append({PARAM_ID: param_id_code[name],
                                        PARAM_VALUE: f"'{val}'",
                                        TIMESTAMP: f"'{timestamp}'",
                                        GEOMETRY: geom})
        return outcome


    @staticmethod
    def pick_last_atmotube_measure_timestamp_from_api_param(api_param: Dict[str, Any]) -> str:

        if "date" not in api_param.keys():
            raise SystemExit(f"{APIPacketPicker.pick_last_atmotube_measure_timestamp_from_api_param.__name__}(): "
                             f"missing 'date' key in Atmotube api parameters.")
        date = ""
        if api_param.get("date", None) is not None:
            date = api_param["date"]
        return date
