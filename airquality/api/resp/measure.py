######################################################
#
# Author: Davide Colombo
# Date: 26/11/21 11:39
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Dict, Any, List
import airquality.api.resp.base as base
import airquality.types.timestamp as ts
import airquality.types.postgis as pgis
import airquality.types.apiresp.measresp as resp


class MeasureBuilder(base.APIRespBuilder, abc.ABC):

    def __init__(self, timestamp_cls):
        self.timestamp_cls = timestamp_cls
        self.channel_name: str = "NO CHANNEL NAME ALREADY SET"

    def with_channel_name(self, channel_name: str):
        self.channel_name = channel_name
        return self


################################ ATMOTUBE API RESPONSE BUILDER ################################
class AtmotubeMeasureBuilder(MeasureBuilder):

    CHANNEL_FIELDS = {"main": ["voc", "pm1", "pm25", "pm10", "t", "h", "p"]}

    def __init__(self, timestamp_cls=ts.AtmotubeTimestamp, postgis_cls=pgis.PostgisPoint):
        super(AtmotubeMeasureBuilder, self).__init__(timestamp_cls=timestamp_cls)
        self.postgis_cls = postgis_cls

    def build(self, parsed_resp: Dict[str, Any]) -> List[resp.MobileSensorAPIResp]:
        responses = []
        try:
            for item in parsed_resp['data']['items']:
                timestamp = self.timestamp_cls(timest=item['time'])
                measures = [resp.ParamNameValue(name=n, value=item.get(n)) for n in self.CHANNEL_FIELDS[self.channel_name]]

                geometry = pgis.NullGeometry()
                if item.get('coords') is not None:
                    geometry = self.postgis_cls(lat=item.get('coords')['lat'], lng=item.get('coords')['lon'])

                responses.append(resp.MobileSensorAPIResp(timestamp=timestamp, measures=measures, geometry=geometry))
        except KeyError as ke:
            raise SystemExit(f"{AtmotubeMeasureBuilder.__name__}: bad API response => missing key={ke!s}")
        return responses


################################ THINGSPEAK API RESPONSE BUILDER ################################
class ThingspeakMeasureBuilder(MeasureBuilder):

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
        super(ThingspeakMeasureBuilder, self).__init__(timestamp_cls=timestamp_cls)

    def build(self, parsed_resp: Dict[str, Any]) -> List[resp.MeasureAPIResp]:
        channel_field_map = self.CHANNEL_FIELDS[self.channel_name]
        responses = []
        try:
            for feed in parsed_resp['feeds']:
                timestamp = self.timestamp_cls(timest=feed['created_at'])

                measures = []
                for field in feed.keys():
                    measures = resp.ParamNameValue(name=channel_field_map[field], value=feed[field])

                responses.append(resp.MeasureAPIResp(timestamp=timestamp, measures=measures))
        except KeyError as ke:
            raise SystemExit(f"{ThingspeakMeasureBuilder.__name__}: bad API response => missing key={ke!s}")
        return responses
