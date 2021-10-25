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
from airquality.constants.shared_constants import EMPTY_LIST, EMPTY_STRING, EMPTY_DICT, \
    PICKER2SQLBUILDER_TIMESTAMP, PICKER2SQLBUILDER_PARAM_ID, PICKER2SQLBUILDER_PARAM_VAL, \
    PICKER2SQLBUILDER_GEOMETRY, GEOMBUILDER_LATITUDE, GEOMBUILDER_LONGITUDE, \
    GEO_TYPE_ST_POINT_2D, ATMOTUBE_DATE_PARAM, PURPLEAIR_NAME_PARAM, PURPLEAIR_SENSOR_IDX_PARAM



class APIPacketPicker(builtins.object):


    @staticmethod
    def pick_atmotube_api_packets_from_last_timestamp_on(packets: List[Dict[str, Any]],
                                                         param_id_code: Dict[str, int],
                                                         last_timestamp: str) -> List[Dict[str, Any]]:
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
        if packets == EMPTY_LIST:
            return outcome

        for packet in packets:
            timestamp = DatetimeParser.atmotube_to_sqltimestamp(packet["time"])
            if not DatetimeParser.is_ts2_after_ts1(ts1 = timestamp, ts2 = last_timestamp):
                geom = "null"
                if "coords" in packet.keys():
                    geom = PostGISGeomBuilder.build_geometry_type(
                            geo_param = {GEOMBUILDER_LONGITUDE: packet["coords"]["lon"],
                                         GEOMBUILDER_LATITUDE: packet["coords"]["lat"]},
                            geo_type = GEO_TYPE_ST_POINT_2D)

                for name, val in packet.items():
                    if name in param_id_code.keys():
                        outcome.append({PICKER2SQLBUILDER_PARAM_ID: param_id_code[name],
                                        PICKER2SQLBUILDER_PARAM_VAL: f"'{val}'",
                                        PICKER2SQLBUILDER_TIMESTAMP: f"'{timestamp}'",
                                        PICKER2SQLBUILDER_GEOMETRY: geom})
        return outcome


    @staticmethod
    def pick_date_from_atmotube_api_param(api_param: Dict[str, Any]) -> str:
        """Static method that returns the value associated to the 'date' key of the 'api_param' argument.

        If 'api_param' is equal to EMPTY_DICT, EMPTY_STRING value is returned.

        If 'date' parameter is missing in 'api_param', SystemExit exception is raised.

        If 'date' is None, EMPTY_STRING value is returned."""

        date = EMPTY_STRING
        if api_param == EMPTY_DICT:
            return date

        if ATMOTUBE_DATE_PARAM not in api_param.keys():
            raise SystemExit(f"{APIPacketPicker.pick_date_from_atmotube_api_param.__name__}(): "
                             f"missing '{ATMOTUBE_DATE_PARAM}' key.")

        if api_param.get("date", None) is not None:
            date = api_param[ATMOTUBE_DATE_PARAM]
        return date


    @staticmethod
    def pick_sensor_name_from_identifier(packet: Dict[str, Any], identifier: str) -> str:
        """Static method that returns the sensor name assembled from the 'packet' based on 'identifier' argument.

        If identifier is invalid, SystemExit exception is raised.

        If key argument(s) for assembling the name is(are) missing, SystemExit exception is raised."""

        keys = packet.keys()

        if identifier == "purpleair":
            if PURPLEAIR_NAME_PARAM not in keys or PURPLEAIR_SENSOR_IDX_PARAM not in keys:
                raise SystemExit(f"{APIPacketPicker.pick_sensor_name_from_identifier.__name__}:"
                                 f"missing '{PURPLEAIR_NAME_PARAM}' or '{PURPLEAIR_SENSOR_IDX_PARAM}' keys.")
            return f"{packet[PURPLEAIR_NAME_PARAM]} ({packet[PURPLEAIR_SENSOR_IDX_PARAM]})"

        else:
            raise SystemExit(f"{APIPacketPicker.pick_sensor_name_from_identifier.__name__}: "
                             f"invalid identifier '{identifier}'.")
