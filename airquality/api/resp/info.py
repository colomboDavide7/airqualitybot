######################################################
#
# Author: Davide Colombo
# Date: 26/11/21 11:09
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict, Any
import airquality.types.apiresp.inforesp as resp
import airquality.api.resp.base as base
import airquality.types.timestamp as ts
import airquality.types.postgis as pgis
import airquality.types.geolocation as geotype
import airquality.types.channel as chtype


class PurpleairSensorInfoBuilder(base.APIRespBuilder):

    TYPE = "Purpleair/Thingspeak"

    CHANNEL_PARAM = [{'name': 'Primary data - Channel A', 'key': 'primary_key_a', 'id': 'primary_id_a'},
                     {'name': 'Primary data - Channel B', 'key': 'primary_key_b', 'id': 'primary_id_b'},
                     {'name': 'Secondary data - Channel A', 'key': 'secondary_key_a', 'id': 'secondary_id_a'},
                     {'name': 'Secondary data - Channel B', 'key': 'secondary_key_b', 'id': 'secondary_id_b'}]

    def __init__(self, timestamp_cls=ts.UnixTimestamp, postgis_cls=pgis.PostgisPoint):
        self.timestamp_cls = timestamp_cls
        self.postgis_cls = postgis_cls

    def build(self, parsed_resp: Dict[str, Any]) -> List[resp.SensorInfoResponse]:
        responses = []
        try:
            for item in parsed_resp['data']:
                # Sensor name
                sensor_name = f"{item['name']} ({item['sensor_index']})"

                # Last acquisition timestamp
                timestamp = self.timestamp_cls(timest=item['date_created'])
                channels = [chtype.Channel(ch_key=item[c['key']], ch_id=item[c['id']], ch_name=c['name'],
                                           last_acquisition=timestamp) for c in self.CHANNEL_PARAM]
                # Geolocation
                geolocation = geotype.Geolocation(timestamp=ts.CurrentTimestamp(),
                                                  geometry=self.postgis_cls(lat=item['latitude'], lng=item['longitude']))

                responses.append(resp.SensorInfoResponse(
                    sensor_name=sensor_name, sensor_type=self.TYPE,channels=channels, geolocation=geolocation)
                )
        except KeyError as ke:
            raise SystemExit(f"{PurpleairSensorInfoBuilder.__name__}: bad API response => missing key={ke!s}")
        return responses
