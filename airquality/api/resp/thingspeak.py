######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 19:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import airquality.api.resp.abc as respabc
import airquality.types.timestamp as tstype


# ------------------------------- ThingspeakAPIRespType ------------------------------- #
class ThingspeakAPIRespType(respabc.MeasureAPIRespTypeABC):

    def __init__(self, item: Dict[str, Any], measure_param: Dict[str, str], timestamp_cls=tstype.ThingspeakTimestamp):
        self.item = item
        self.measure_param = measure_param
        self.timestamp_cls = timestamp_cls

    def measured_at(self) -> tstype.Timestamp:
        try:
            return self.timestamp_cls(timest=self.item['created_at'])
        except KeyError as err:
            raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} exception in {self.measured_at.__name__} => {err!r}")

    def measures(self) -> List[respabc.NameValue]:
        try:
            return [respabc.NameValue(name=self.measure_param[param], value=self.item.get(param)) for param in self.measure_param]
        except KeyError as err:
            raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} exception in {self.measures.__name__} => {err!r}")

    def located_at(self):
        raise SystemExit(f"{self.__class__.__name__} in {self.located_at.__name__}: => this method is not allowed for this class...")


# ------------------------------- ThingspeakAPIRespBuilder ------------------------------- #
class ThingspeakAPIRespBuilder(respabc.APIRespBuilderABC):

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

    def __init__(self, channel_name: str, timestamp_cls=tstype.ThingspeakTimestamp):
        self.channel_name = channel_name
        self.timestamp_cls = timestamp_cls

    ################################ build ################################
    def build(self, parsed_resp: Dict[str, Any]) -> List[ThingspeakAPIRespType]:
        try:
            feeds = parsed_resp['feeds']
            measure_param = self.CHANNEL_FIELDS[self.channel_name]
            return [ThingspeakAPIRespType(item=feed, measure_param=measure_param, timestamp_cls=self.timestamp_cls) for feed in feeds]
        except KeyError as kerr:
            raise SystemExit(f"{self.__class__.__name__} catches {kerr.__class__.__name__} => {kerr!s}")
