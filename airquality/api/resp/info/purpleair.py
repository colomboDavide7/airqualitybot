######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 18:55
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict, Any
import airquality.api.resp.info.info as base
import airquality.types.apiresp.inforesp as rtype
import airquality.types.timestamp as ts
import airquality.types.postgis as pgis
import airquality.types.geolocation as geotype
import airquality.types.channel as chtype


class PurpleairAPIRespBuilder(base.InfoAPIRespBuilder):
    TYPE = "Purpleair/Thingspeak"

    CHANNEL_PARAM = [{'name': 'Primary data - Channel A', 'key': 'primary_key_a', 'id': 'primary_id_a'},
                     {'name': 'Primary data - Channel B', 'key': 'primary_key_b', 'id': 'primary_id_b'},
                     {'name': 'Secondary data - Channel A', 'key': 'secondary_key_a', 'id': 'secondary_id_a'},
                     {'name': 'Secondary data - Channel B', 'key': 'secondary_key_b', 'id': 'secondary_id_b'}]

    def __init__(self, timestamp_cls=ts.UnixTimestamp, postgis_cls=pgis.PostgisPoint):
        self.timestamp_cls = timestamp_cls
        self.postgis_cls = postgis_cls

    ################################ build() ################################
    def build(self, parsed_resp: Dict[str, Any]) -> List[rtype.SensorInfoResponse]:
        self.exit_on_bad_parsed_response(parsed_resp)
        responses = []
        for data in parsed_resp['data']:
            item = dict(zip(parsed_resp['fields'], data))
            self.exit_on_bad_item(item)
            sensor_name = self.get_sensor_name(item)
            channels = self.get_channels(item)
            geolocation = self.get_geolocation(item)
            responses.append(rtype.SensorInfoResponse(
                sensor_name=sensor_name, sensor_type=self.TYPE, channels=channels, geolocation=geolocation)
            )
        return responses

    ################################ get_sensor_name() ################################
    def get_sensor_name(self, item: Dict[str, Any]) -> str:
        return f"{item['name']} ({item['sensor_index']})".replace("'", "")

    ################################ get_channels() ################################
    def get_channels(self, item: Dict[str, Any]) -> List[chtype.Channel]:
        timestamp = self.timestamp_cls(timest=item['date_created'])
        channels = []
        for c in self.CHANNEL_PARAM:
            ch = chtype.Channel(ch_key=item[c['key']], ch_id=item[c['id']], ch_name=c['name'], last_acquisition=timestamp)
            channels.append(ch)
        return channels

    ################################ get_geolocation() ################################
    def get_geolocation(self, item: Dict[str, Any]) -> geotype.Geolocation:
        return geotype.Geolocation(
            timestamp=ts.CurrentTimestamp(), geometry=self.postgis_cls(lat=item['latitude'], lng=item['longitude'])
        )

    ################################ exit_on_bad_item ################################
    def exit_on_bad_item(self, item: Dict[str, Any]) -> None:
        msg_header = f"{PurpleairAPIRespBuilder.__name__}: bad response item =>"
        err_msg = ""
        if 'name' not in item:
            err_msg = f"{msg_header} missing key='name'"
        if 'sensor_index' not in item:
            err_msg = f"{msg_header} missing key='sensor_index'"
        if 'date_created' not in item:
            err_msg = f"{msg_header} missing key='date_created'"
        if 'latitude' not in item:
            err_msg = f"{msg_header} missing key='latitude'"
        if 'longitude' not in item:
            err_msg = f"{msg_header} missing key='longitude'"

        for c in self.CHANNEL_PARAM:
            if c['key'] not in item:
                err_msg = f"{msg_header} missing key='{c['key']}'"
            if c['id'] not in item:
                err_msg = f"{msg_header} missing key='{c['id']}'"

        if err_msg != "":
            raise SystemExit(err_msg)

    ################################ exit_on_bad_parsed_response ################################
    def exit_on_bad_parsed_response(self, parsed_resp: Dict[str, Any]) -> None:
        if 'fields' not in parsed_resp:
            raise SystemExit(f"{PurpleairAPIRespBuilder.__name__}: bad parsed response => missing 'fields' section")
        if 'data' not in parsed_resp:
            raise SystemExit(f"{PurpleairAPIRespBuilder.__name__}: bad parsed response => missing 'data' section")
