######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 11:54
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List
import airquality.api.resp.resp as resp
import airquality.types.measure as measuretype
import airquality.types.timestamp as ts
import airquality.types.postgis as pgis
import airquality.types.info as infotype
import airquality.types.channel as chtype
import airquality.types.geolocation as geotype


class APIRespAdapt(abc.ABC):

    @abc.abstractmethod
    def adapt(self, api_resp):
        pass


################################ ATMOTUBE API RESPONSE ADAPTER ################################
class AtmoAPIRespAdapt(APIRespAdapt):

    def __init__(self, measure_id_name: List[sel.ParamNameID], timestamp_cls=ts.AtmotubeTimestamp, postgis_cls=pgis.PostgisPoint):
        self.timestamp_cls = timestamp_cls
        self.postgis_cls = postgis_cls
        self.measure_id_name = measure_id_name

    def adapt(self, api_resp: List[resp.MobileSensorAPIResp]) -> List[measuretype.MobileMeasure]:
        adapted_resp = []
        for r in api_resp:
            adapted_resp.append(
                measuretype.MobileMeasure(
                    measures=self._get_measures(r),
                    geometry=self.postgis_cls(lat=r.lat, lng=r.lon),
                    timestamp=self.timestamp_cls(r.time)
                )
            )
        return adapted_resp

    def _get_measures(self, r: resp.MobileSensorAPIResp) -> List[measuretype.ParamIDValue]:
        measure_dict = {}
        for m in self.measure_id_name:
            measure_dict[m.name] = m.id
        return [measuretype.ParamIDValue(id_=measure_dict[m.name], value=m.value) for m in r.measures]


################################ PURPLEAIR API RESPONSE ADAPTER ################################
class PurpAPIRespAdpt(APIRespAdapt):

    def __init__(self, timestamp_cls=ts.UnixTimestamp, postgis_cls=pgis.PostgisPoint):
        self.timestamp_cls = timestamp_cls
        self.postgis_cls = postgis_cls

    def adapt(self, api_resp: List[resp.PurpAPIResp]) -> List[infotype.StationInfo]:
        adapted_resp = []
        for r in api_resp:
            adapted_resp.append(
                infotype.StationInfo(
                    sensor_name=f"{r.name} ({r.sensor_index})".replace("'", ""),
                    sensor_type=r.TYPE,
                    geolocation=self._get_geolocation(r),
                    ch_param=self._get_channel_param(r))
            )
        return adapted_resp

    def _get_channel_param(self, r: resp.PurpAPIResp) -> List[chtype.Channel]:
        return [chtype.Channel(ch_id=r.data[c['id']], ch_key=r.data[c['key']], ch_name=c['name'],
                               last_acquisition=self.timestamp_cls(r.date_created)) for c in r.CHANNEL_PARAM]

    def _get_geolocation(self, r: resp.PurpAPIResp) -> geotype.Geolocation:
        return geotype.Geolocation(timestamp=ts.CurrentTimestamp(), geometry=self.postgis_cls(lat=r.latitude, lng=r.longitude))


################################ THINGSPEAK API RESPONSE ADAPTER ################################
class ThnkAPIRespAdapt(APIRespAdapt):

    def __init__(self, measure_id_name: List[sel.ParamNameID], timestamp_cls=ts.ThingspeakTimestamp):
        self.measure_id_name = measure_id_name
        self.timestamp_cls = timestamp_cls

    def adapt(self, api_resp: List[resp.THNKRESPTYPE]) -> List[measuretype.StationMeasure]:
        adapted_resp = []
        for r in api_resp:
            adapted_resp.append(
                measuretype.StationMeasure(
                    timestamp=self.timestamp_cls(timest=r.created_at),
                    measures=self._get_measures(r)
                )
            )
        return adapted_resp

    def _get_measures(self, r: resp.THNKRESPTYPE) -> List[measuretype.ParamIDValue]:
        measure_dict = {}
        for m in self.measure_id_name:
            measure_dict[m.name] = m.id
        return [measuretype.ParamIDValue(id_=measure_dict[m.name], value=m.value) for m in r.measures]
