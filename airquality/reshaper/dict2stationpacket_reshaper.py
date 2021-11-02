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
from airquality.api2database.measurement_packet import StationMeasurementPacket
from airquality.constants.shared_constants import EMPTY_LIST, EMPTY_DICT, THINGSPEAK_API_RESHAPER_TIME


class Dict2StationpacketReshaper(ABC):

    @abstractmethod
    def reshape_packets(self, packets: List[Dict[str, Any]], sensor_id: int, measure_param_map: Dict[str, Any]
                        ) -> List[StationMeasurementPacket]:
        pass


class Dict2StationpacketReshaperThingspeak(Dict2StationpacketReshaper):

    def reshape_packets(self, packets: List[Dict[str, Any]], sensor_id: int, measure_param_map: Dict[str, Any]
                        ) -> List[StationMeasurementPacket]:

        if packets == EMPTY_LIST:
            return []

        if measure_param_map == EMPTY_DICT:
            raise SystemExit(f"{Dict2StationpacketReshaperThingspeak.__name__}: cannot reshape packets when reshape "
                             f"mapping is empty.")

        reshaped_packets = []
        for packet in packets:
            timestamp = packet[THINGSPEAK_API_RESHAPER_TIME]
            for name, val in packet.items():
                if name in measure_param_map.keys():
                    reshaped_packets.append(StationMeasurementPacket(param_id=measure_param_map[name],
                                                                     sensor_id=sensor_id,
                                                                     param_val=val,
                                                                     timestamp=timestamp))
        return reshaped_packets


################################ FACTORY ################################
class Dict2StationpacketReshaperFactory(builtins.object):

    @classmethod
    def create_reshaper(cls, bot_personality: str) -> Dict2StationpacketReshaper:

        if bot_personality == "thingspeak":
            return Dict2StationpacketReshaperThingspeak()
        else:
            raise SystemExit(f"{Dict2StationpacketReshaperFactory.__name__}: cannot instantiate "
                             f"{Dict2StationpacketReshaper.__name__} instance for personality='{bot_personality}'.")
