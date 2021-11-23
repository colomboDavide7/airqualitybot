######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 17:06
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict, Any
import airquality.api.model.thingspeak as thk_mdl
import airquality.api.model.atmotube as atm_mdl
import airquality.adapter.api2db.base as base
import airquality.database.util.datatype.timestamp as ts
import airquality.database.util.postgis.geom as geo


class FetchUniformModel(base.BaseUniformModel):

    def __init__(self, timestamp: ts.Timestamp, parameters: List[base.ParamIDValue], geolocation=geo.NullGeometry()):
        self.timestamp = timestamp
        self.parameters = parameters
        self.geolocation = geolocation


################################ FETCH ADAPTERS ###############################
class FetchAPI2DBAdapter(base.BaseAPI2DBAdapter, abc.ABC):

    def __init__(self, measure_param_map: Dict[str, Any], timestamp_class=ts.Timestamp):
        self.measure_param_map = measure_param_map
        self.timestamp_class = timestamp_class


################################ ATMOTUBE FETCH ADAPTER ###############################
class AtmotubeFetchAPI2DBAdapter(FetchAPI2DBAdapter):

    def __init__(self, measure_param_map: Dict[str, Any], timestamp_class=ts.AtmotubeTimestamp, postgis_class=geo.PostgisPoint):
        super(AtmotubeFetchAPI2DBAdapter, self).__init__(measure_param_map=measure_param_map, timestamp_class=timestamp_class)
        self.postgis_class = postgis_class

    def adapt(self, responses: List[atm_mdl.AtmotubeResponseModel]) -> List[base.BaseUniformModel]:
        uniformed_responses = []
        for response in responses:
            timestamp = self.timestamp_class(timest=response.time)
            parameters = [base.ParamIDValue(id_=self.measure_param_map[p.name], value=p.value) for p in response.parameters]
            geolocation = geo.NullGeometry()
            if response.lat is not None and response.lon is not None:
                geolocation = self.postgis_class(lat=response.lat, lng=response.lon)
            uniformed_responses.append(FetchUniformModel(timestamp=timestamp, parameters=parameters, geolocation=geolocation))
        return uniformed_responses


################################ THINGSPEAK FETCH ADAPTER ###############################
class ThingspeakFetchAPI2DBAdapter(FetchAPI2DBAdapter):

    def __init__(self, measure_param_map: Dict[str, Any], timestamp_class=ts.ThingspeakTimestamp):
        super(ThingspeakFetchAPI2DBAdapter, self).__init__(measure_param_map=measure_param_map, timestamp_class=timestamp_class)

    def adapt(self, responses: List[thk_mdl.RESP_MODEL_TYPE]) -> List[base.BaseUniformModel]:
        uniformed_responses = []
        for response in responses:
            timestamp = self.timestamp_class(timest=response.created_at)
            parameters = [base.ParamIDValue(id_=self.measure_param_map[p.name], value=p.value) for p in response.parameters]
            uniformed_responses.append(FetchUniformModel(timestamp=timestamp, parameters=parameters))
        return uniformed_responses
