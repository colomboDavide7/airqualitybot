#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 11:47
# @Description: this script defines the classes for picking sensor's API packet values
#
#################################################
import builtins
from typing import Dict, Any
from airquality.constants.shared_constants import PURPLEAIR_NAME_PARAM, PURPLEAIR_SENSOR_IDX_PARAM



class APIPacketPicker(builtins.object):


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
