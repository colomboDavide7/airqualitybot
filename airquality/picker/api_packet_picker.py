#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 11:47
# @Description: this script defines the classes for picking sensor's API packet values
#
#################################################
import builtins
from typing import Dict, Any, List
from airquality.app import EMPTY_STRING, EMPTY_LIST
from airquality.parser.datetime_parser import DatetimeParser
from airquality.geom.postgis_geom_builder import PostGISGeomBuilder
from airquality.picker import TIMESTAMP, PARAM_VALUE, PARAM_ID, GEOMETRY


class APIPacketPicker(builtins.object):

    """This parameter are defined within the APIPacketPicker class and are used for building the output
    dictionary from the methods. The SQLQueryBuilder will use this variables to unpack the dictionary and
    create a query from it."""


    @staticmethod
    def pick_atmotube_api_packets_from_last_timestamp_on(
        parsed_api_answer: List[Dict[str, Any]],
        param_id_code: Dict[str, int],
        last_timestamp: str
    ) -> List[Dict[str, Any]]:
        """Static method that returns a list of dictionaries. Each dictionary contains the key-value for inserting
        measurement into the database.

        The dictionary keys are taken from (TIMESTAMP, PARAM_VALUE, PARAM_ID, GEOMETRY).
        This is done in order to ensure that other methods that takes the packets outputted by this method as argument,
        can understand the structure.

        The purpose of this method is to assemble a valid packet from the list of parsed packets taken from the APIs.

        Each packet if translated in the form:
            - param_id:     the id of the parameter taken from the 'param_id_code' argument.
            - param_value:  the value of the parameter associated to the 'param_id'
            - timestamp:    the current measure timestamp taken from the packet
            - geometry:     the geometry object associated to the measure (POINT)

        This structure is related to database tables."""

        outcome = EMPTY_LIST

        for packet in parsed_api_answer:
            timestamp = DatetimeParser.parse_atmotube_timestamp(packet["time"])
            if not DatetimeParser.is_ts1_before_ts2(ts1 = timestamp, ts2 = last_timestamp):
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
    def pick_last_atmotube_measure_timestamp_or_empty_string(api_param: Dict[str, Any]) -> str:
        """Static method which purpose is to return the 'date' value from the atmotube sensor 'api_param' argument.

        If no 'date' key is present in 'api_param' dictionary, SystemExit exception is raised.

        If 'date' value is None, an empty string is returned.

        The 'date' value is None if it is the first acquisition for the Atmotube sensor associated to the 'api_param'."""

        if "date" not in api_param.keys():
            raise SystemExit(f"{APIPacketPicker.pick_last_atmotube_measure_timestamp_or_empty_string.__name__}(): "
                             f"missing 'date' key in Atmotube api parameters.")
        date = EMPTY_STRING
        if api_param.get("date", None) is not None:
            date = api_param["date"]
        return date


    @staticmethod
    def reshape_purpleair_api_packets(parsed_api_answer: Dict[str, Any]) -> List[Dict[str, Any]]:

        reshaped_packets = []
        n_fields = len(parsed_api_answer["fields"])

        if parsed_api_answer["data"] != EMPTY_LIST:
            for data in parsed_api_answer["data"]:
                packet = {}
                for i in range(n_fields):
                    key = parsed_api_answer["fields"][i]
                    val = data[i]
                    packet[key] = val

                reshaped_packets.append(packet)

        return reshaped_packets

