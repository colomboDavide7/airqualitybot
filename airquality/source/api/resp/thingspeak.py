######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 19:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import airquality.source.api.resp.abc as respabc


CHANNEL_FIELDS = {
        "Primary data - Channel A": {
            "field1": "pm1.0_atm_a", "field2": "pm2.5_atm_a", "field3": "pm10.0_atm_a",
            "field6": "temperature_a", "field7": "humidity_a"
        }, "Primary data - Channel B": {
            "field1": "pm1.0_atm_b", "field2": "pm2.5_atm_b", "field3": "pm10.0_atm_b", "field6": "pressure_b"
        }, "Secondary data - Channel A": {
            "field1": "0.3_um_count_a", "field2": "0.5_um_count_a", "field3": "1.0_um_count_a",
            "field4": "2.5_um_count_a", "field5": "5.0_um_count_a", "field6": "10.0_um_count_a"
        }, "Secondary data - Channel B": {
            "field1": "0.3_um_count_b", "field2": "0.5_um_count_b", "field3": "1.0_um_count_b",
            "field4": "2.5_um_count_b", "field5": "5.0_um_count_b", "field6": "10.0_um_count_b"
        }
    }


# ------------------------------- ThingspeakAPIRespType ------------------------------- #
class ThingspeakAPIRespType(respabc.APIRespTypeABC):

    def __init__(self, item: Dict[str, Any], channel_name: str):
        self.item = item
        self.channel_name = channel_name

    @property
    def created_at(self) -> str:
        return self.item['created_at']

    @property
    def measures(self) -> List[respabc.NameValue]:
        channel_field_map = CHANNEL_FIELDS[self.channel_name]
        return [respabc.NameValue(name=channel_field_map[param], value=self.item.get(param)) for param in channel_field_map]


# ------------------------------- ThingspeakAPIRespBuilder ------------------------------- #
class ThingspeakAPIRespBuilder(respabc.APIRespBuilderABC):

    def __init__(self, channel_name: str):
        self.channel_name = channel_name

    ################################ build ################################
    def build(self, parsed_resp: Dict[str, Any]) -> List[ThingspeakAPIRespType]:
        feeds = parsed_resp['feeds']
        return [ThingspeakAPIRespType(item=feed, channel_name=self.channel_name) for feed in feeds]
