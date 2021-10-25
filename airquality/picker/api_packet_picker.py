#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 11:47
# @Description: this script defines the classes for picking sensor's API packet values
#
#################################################
import builtins
from typing import Dict, Any, List
from airquality.constants.shared_constants import EMPTY_LIST, EMPTY_STRING
from airquality.geom import GEO_TYPE_ST_POINT_2D
from airquality.parser.datetime_parser import DatetimeParser
from airquality.geom.postgis_geom_builder import PostGISGeomBuilderFactory
from airquality.picker import TIMESTAMP, PARAM_VALUE, PARAM_ID, GEOMETRY, PURPLE_AIR_API_PARAM, PURPLE_AIR_GEO_PARAM


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
            timestamp = DatetimeParser.atmotube_to_sqltimestamp(packet["time"])
            if not DatetimeParser.is_ts2_after_ts1(ts1 = timestamp, ts2 = last_timestamp):
                geom = "null"
                if "coords" in packet.keys():
                    geo_factory = PostGISGeomBuilderFactory()
                    geo_builder = geo_factory.create_posGISGeomBuilder(bot_personality = "atmotube")
                    geom = geo_builder.build_geometry_type(geo_param = {"longitude": packet["coords"]["lon"],
                                                                        "latitude": packet["coords"]["lat"]},
                                                           geo_type = GEO_TYPE_ST_POINT_2D)

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
    def pick_sensor_name_from_identifier(packet: Dict[str, Any], identifier: str) -> str:

        if identifier == "purpleair":
            if "name" not in packet.keys() or "sensor_index" not in packet.keys():
                raise SystemExit(f"{APIPacketPicker.pick_sensor_name_from_identifier.__name__}:"
                                 f"missing 'name' or 'sensor_index' keys in purpleair packet.")

            return f"{packet['name']} ({packet['sensor_index']})"

        else:
            raise SystemExit(f"{APIPacketPicker.pick_sensor_name_from_identifier.__name__}: "
                             f"invalid identifier '{identifier}'.")

    @staticmethod
    def pick_api_param_from_packet(packet: Dict[str, Any], identifier: str) -> Dict[str, Any]:

        api_param = {}
        if identifier == "purpleair":

            for param in PURPLE_AIR_API_PARAM:
                if param not in packet.keys():
                    raise SystemExit(f"{APIPacketPicker.pick_api_param_from_packet.__name__}: "
                                     f"missing required api param '{param}' for '{identifier}'.")
                api_param[param] = packet[param]

        else:
            raise SystemExit(f"{APIPacketPicker.pick_api_param_from_packet.__name__}: "
                             f"invalid identifier '{identifier}'.")

        return api_param


    @staticmethod
    def pick_geometry_from_packet(packet: Dict[str, Any], identifier: str) -> str:

        geo_param = {}
        geo_factory = PostGISGeomBuilderFactory()
        if identifier == "purpleair":
            for param in PURPLE_AIR_GEO_PARAM:
                if param not in packet.keys():
                    raise SystemExit(f"{APIPacketPicker.pick_geometry_from_packet.__name__}: "
                                     f"missing required geo param '{param}' for '{identifier}'.")
                geo_param[param] = str(packet[param])

            geo_builder = geo_factory.create_posGISGeomBuilder(bot_personality = identifier)
            geom = geo_builder.build_geometry_type(geo_param = geo_param, geo_type = GEO_TYPE_ST_POINT_2D)
        else:
            raise SystemExit(f"{APIPacketPicker.pick_api_param_from_packet.__name__}: "
                             f"invalid identifier '{identifier}'.")
        return geom
