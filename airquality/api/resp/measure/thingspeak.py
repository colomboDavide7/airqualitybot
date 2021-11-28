######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 19:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import airquality.api.resp.measure.measure as base
import airquality.types.timestamp as ts
import airquality.types.apiresp.measresp as resp


class ThingspeakAPIRespBuilder(base.MeasureAPIRespBuilder):

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

    def __init__(self, timestamp_cls=ts.ThingspeakTimestamp):
        super(ThingspeakAPIRespBuilder, self).__init__(timestamp_cls=timestamp_cls)

    ################################ build ################################
    def build(self, parsed_resp: Dict[str, Any]) -> List[resp.MeasureAPIResp]:
        self.exit_on_missing_channel_name()
        self.exit_on_bad_parsed_response(parsed_resp)
        responses = []
        for item in parsed_resp['feeds']:
            self.exit_on_bad_item(item)
            timestamp = self.timestamp_cls(timest=item['created_at'])
            measures = self.get_measures(item=item)
            responses.append(resp.MeasureAPIResp(timestamp=timestamp, measures=measures))
        return responses

    ################################ get_measures ################################
    def get_measures(self, item: Dict[str, Any]) -> List[resp.ParamNameValue]:
        channel_field_map = self.CHANNEL_FIELDS[self.channel_name]
        measures = []
        for field in channel_field_map.keys():
            measures.append(resp.ParamNameValue(name=channel_field_map[field], value=item.get(field)))
        return measures

    ################################ exit_on_bad_item ################################
    def exit_on_bad_item(self, item: Dict[str, Any]) -> None:
        if 'created_at' not in item:
            raise SystemExit(f"{ThingspeakAPIRespBuilder.__name__}: bad response item => missing key='created_at'")

        for field in self.CHANNEL_FIELDS[self.channel_name]:
            if field not in item:
                raise SystemExit(f"{ThingspeakAPIRespBuilder.__name__}: bad response item => missing key='{field}'")

    ################################ exit_on_bad_parsed_data ################################
    def exit_on_bad_parsed_response(self, parsed_resp: Dict[str, Any]) -> None:
        if 'feeds' not in parsed_resp:
            raise SystemExit(f"{ThingspeakAPIRespBuilder.__name__}: bad parsed response => missing 'feeds' section")
