######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 19:21
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import source.api.resp.measure.measure as base
import airquality.types.apiresp.measresp as resp
import airquality.types.timestamp as ts
import airquality.types.postgis as pgis


class AtmotubeAPIRespBuilder(base.MeasureAPIRespBuilder):

    CHANNEL_FIELDS = {"main": ["voc", "pm1", "pm25", "pm10", "t", "h", "p"]}

    def __init__(self, timestamp_cls=ts.AtmotubeTimestamp, postgis_cls=pgis.PostgisPoint):
        super(AtmotubeAPIRespBuilder, self).__init__(timestamp_cls=timestamp_cls)
        self.postgis_cls = postgis_cls

    ################################ build ################################
    def build(self, parsed_resp: Dict[str, Any]) -> List[resp.MobileSensorAPIResp]:
        self.exit_on_missing_channel_name()
        self.exit_on_bad_parsed_response(parsed_resp)
        responses = []
        for item in parsed_resp['data']['items']:
            self.exit_on_bad_item(item)
            timestamp = self.timestamp_cls(timest=item['time'])
            measures = self.get_measures(item=item)
            geometry = self.get_geometry(item)
            responses.append(resp.MobileSensorAPIResp(timestamp=timestamp, measures=measures, geometry=geometry))
        return responses

    ################################ get_measures ################################
    def get_measures(self, item: Dict[str, Any]) -> List[resp.ParamNameValue]:
        channel_field_map = self.CHANNEL_FIELDS[self.channel_name]
        return [resp.ParamNameValue(name=n, value=item.get(n)) for n in channel_field_map]

    ################################ get_geometry ################################
    def get_geometry(self, item: Dict[str, Any]) -> pgis.PostgisPoint:
        geometry = pgis.NullGeometry()
        if item.get('coords') is not None:
            geometry = self.postgis_cls(lat=item.get('coords')['lat'], lng=item.get('coords')['lon'])
        return geometry

    ################################ exit_on_bad_item ################################
    def exit_on_bad_item(self, item: Dict[str, Any]) -> None:
        if 'time' not in item:
            raise SystemExit(f"{AtmotubeAPIRespBuilder.__name__}: bad response item => missing key='time'")

    ################################ exit_on_bad_parsed_response ################################
    def exit_on_bad_parsed_response(self, parsed_resp: Dict[str, Any]) -> None:
        if 'data' not in parsed_resp:
            raise SystemExit(f"{AtmotubeAPIRespBuilder.__name__}: bad parsed response => missing 'data' section")
        if 'items' not in parsed_resp['data']:
            raise SystemExit(f"{AtmotubeAPIRespBuilder.__name__}: bad parsed response => missing 'item' section")
