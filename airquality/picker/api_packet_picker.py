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
    GEO_TYPE_ST_POINT_2D, ATMOTUBE_DATE_PARAM, PURPLEAIR_NAME_PARAM, PURPLEAIR_SENSOR_IDX_PARAM, \
    ATMOTUBE_TIME_PARAM, ATMOTUBE_COORDS_PARAM



class APIPacketPicker(builtins.object):


    @classmethod
    def reshape_atmotube_packets(cls, packets: List[Dict[str, Any]], paramcode2paramid_map: Dict[str, int]
                                 ) -> List[Dict[str, Any]]:
        """Class method that takes a list of packets from an atmotube sensor API and reshape each packet in order
        to be compliant with the strucure of the 'mobile_measurement' table in the database.

        If packets is equal to EMPTY_LIST, EMPTY_LIST value is returned."""

        outcome = EMPTY_LIST
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
                if name in paramcode2paramid_map.keys():
                    outcome.append({PICKER2SQLBUILDER_PARAM_ID: paramcode2paramid_map[name],
                                    PICKER2SQLBUILDER_PARAM_VAL: f"'{val}'",
                                    PICKER2SQLBUILDER_TIMESTAMP: f"'{timestamp}'",
                                    PICKER2SQLBUILDER_GEOMETRY: geom})
        return outcome


    @classmethod
    def pick_date_from_api_param_by_identifier(cls, api_param: Dict[str, Any], identifier: str) -> str:
        """Static method that returns the value associated to the 'date' key of the 'api_param' argument.

        If 'api_param' is equal to EMPTY_DICT, EMPTY_STRING value is returned.
        If 'date' parameter is missing in 'api_param', SystemExit exception is raised.
        If 'date' is None, EMPTY_STRING value is returned."""

        date = EMPTY_STRING
        if api_param == EMPTY_DICT:
            return date

        if identifier == "atmotube":

            if ATMOTUBE_DATE_PARAM not in api_param.keys():
                raise SystemExit(f"{APIPacketPicker.pick_date_from_api_param_by_identifier.__name__}(): "
                                 f"missing '{ATMOTUBE_DATE_PARAM}' key.")

            if api_param.get(ATMOTUBE_DATE_PARAM, None) is not None:
                date = api_param[ATMOTUBE_DATE_PARAM]
        else:
            raise SystemExit(f"{APIPacketPicker.pick_date_from_api_param_by_identifier.__name__}:"
                             f"invalid personality '{identifier}'.")

        return date


    @classmethod
    def pick_sensor_name_from_identifier(cls, packet: Dict[str, Any], identifier: str) -> str:
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


    @classmethod
    def pick_packet_timestamp_from_identifier(cls, packet: Dict[str, Any], identifier: str):
        """Class method that returns the parsed sql timestamp from the packet based on identifier argument.

        If timestamp param is missing from the packet, SystemExit exception is raised.
        If 'identifier' is not recognized, SystemExit exception is raised. """

        keys = packet.keys()

        if identifier == "atmotube":
            if ATMOTUBE_TIME_PARAM not in keys:
                raise SystemExit(f"{APIPacketPicker.pick_packet_timestamp_from_identifier.__name__}: "
                                 f"missing '{ATMOTUBE_TIME_PARAM}' key.")
            return DatetimeParser.atmotube_to_sqltimestamp(ts = packet[ATMOTUBE_TIME_PARAM])
        else:
            raise SystemExit(f"{APIPacketPicker.pick_packet_timestamp_from_identifier.__name__}: "
                             f"invalid identifier '{identifier}'.")
