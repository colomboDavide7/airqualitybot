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


class APIPacketPicket(builtins.object):

    """This parameter are defined within the APIPacketPicker class and are used for building the output
    dictionary from the methods. The SQLQueryBuilder will use this variables to unpack the dictionary and
    create a query from it."""


    PARAM_ID  = "par_id"
    SENSOR_ID = "sens_id"
    PARAM_VALUE = "par_val"
    TIMESTAMP = "ts"


    @staticmethod
    def pick_atmotube_api_packet(
        parsed_api_answer: List[Dict[str, Any]],
        param_id_code: Dict[str, int],
        sensor_id: int
    ) -> List[Dict[str, Any]]:

        outcome = []

        for packet in parsed_api_answer:
            timestamp = DatetimeParser.parser_atmotube_timestamp(packet["time"])
            for name, val in packet.items():
                if name in param_id_code.keys():
                    outcome.append({APIPacketPicket.PARAM_ID: param_id_code[name],
                                    APIPacketPicket.SENSOR_ID: sensor_id,
                                    APIPacketPicket.PARAM_VALUE: f"'{val}'",
                                    APIPacketPicket.TIMESTAMP: f"'{timestamp}'"})
        return outcome
