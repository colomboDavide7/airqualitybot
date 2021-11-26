######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 12:00
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.api2db.adptype as adptype
import airquality.api2db.adpt as adpt
import airquality.api.resp.resp as resp
import airquality.database.ext.postgis as pgis
import airquality.database.dtype.timestamp as ts


class PurpAPIRespAdpt(adpt.APIRespAdapt):

    def __init__(self, timestamp_cls=ts.UnixTimestamp, postgis_cls=pgis.PostgisPoint):
        self.timestamp_cls = timestamp_cls
        self.postgis_cls = postgis_cls

    def adapt(self, api_resp: List[resp.PurpAPIResp]) -> List[adptype.StationInfo]:
        adapted_resp = []
        for r in api_resp:
            adapted_resp.append(
                adptype.StationInfo(
                    sensor_name=f"{r.name} ({r.sensor_index})".replace("'", ""),
                    sensor_type=r.TYPE,
                    geolocation=self._get_geolocation(r),
                    ch_param=self._get_channel_param(r))
            )
        return adapted_resp

    def _get_channel_param(self, r: resp.PurpAPIResp) -> List[adptype.ChannelParam]:
        return [adptype.ChannelParam(
            ch_id=r.data[c['id']], ch_key=r.data[c['key']], ch_name=c['name'], last_acquisition=self.timestamp_cls(r.date_created)
            ) for c in r.CHANNEL_PARAM]

    def _get_geolocation(self, r: resp.PurpAPIResp) -> adptype.Geolocation:
        return adptype.Geolocation(timestamp=ts.CurrentTimestamp(),
                                   geometry=self.postgis_cls(lat=r.latitude, lng=r.longitude))
