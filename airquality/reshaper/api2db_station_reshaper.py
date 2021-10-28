#################################################
#
# @Author: davidecolombo
# @Date: mer, 27-10-2021, 20:52
# @Description: this script defines the classes for reshaping api packets in order to make them compliant to the
#               database needs during the packets insertion.
#
#               This script is specific for 'station_measurement' that need the 'sensor_id'
#
#################################################
import builtins
from typing import Dict, Any, List
from abc import ABC, abstractmethod
from airquality.constants.shared_constants import EMPTY_LIST, EMPTY_DICT, \
    RESHAPER2SQLBUILDER_TIMESTAMP, RESHAPER2SQLBUILDER_SENSOR_ID, RESHAPER2SQLBUILDER_PARAM_VAL, RESHAPER2SQLBUILDER_PARAM_ID, \
    THINGSPEAK_API_RESHAPER_TIME


class API2DatabaseStationReshaper(ABC):


    @abstractmethod
    def reshape_packets(self, packets: List[Dict[str, Any]], sensor_id: int, measure_param_map: Dict[str, Any]
                        ) -> List[Dict[str, Any]]:
        pass



class API2DatabaseStationReshaperThingspeak(API2DatabaseStationReshaper):


    def reshape_packets(self, packets: List[Dict[str, Any]], sensor_id: int, measure_param_map: Dict[str, Any]
                        ) -> List[Dict[str, Any]]:

        if packets == EMPTY_LIST:
            return []

        if measure_param_map == EMPTY_DICT:
            raise SystemExit(f"{API2DatabaseStationReshaperThingspeak.__name__}: cannot reshape packets when reshape "
                             f"mapping is empty.")

        reshaped_packets = []
        for packet in packets:
            timestamp = packet[THINGSPEAK_API_RESHAPER_TIME]
            for name, val in packet.items():
                if name in measure_param_map.keys():
                    reshaped_packets.append({RESHAPER2SQLBUILDER_PARAM_ID: measure_param_map[name],
                                             RESHAPER2SQLBUILDER_SENSOR_ID: sensor_id,
                                             RESHAPER2SQLBUILDER_PARAM_VAL: f"'{val}'",
                                             RESHAPER2SQLBUILDER_TIMESTAMP: f"'{timestamp}'"})
        return reshaped_packets


################################ FACTORY ################################
class API2DatabaseStationReshaperFactory(builtins.object):


    @classmethod
    def create_reshaper(cls, bot_personality: str) -> API2DatabaseStationReshaper:

        if bot_personality == "thingspeak":
            return API2DatabaseStationReshaperThingspeak()
        else:
            raise SystemExit(f"{API2DatabaseStationReshaperFactory.__name__}: cannot instantiate "
                             f"{API2DatabaseStationReshaper.__name__} instance for personality='{bot_personality}'.")
