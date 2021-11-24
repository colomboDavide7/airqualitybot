######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:58
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import airquality.api.resp.atmresp as atm_mdl
import airquality.database.postgis.geom as geo
import airquality.database.datatype.timestamp as ts
import airquality.api2db.fetchunif.fetchunif as baseadapt


class AtmotubeUniformResponseBuilder(baseadapt.FetchUniformResponseBuilder):

    def __init__(self, measure_param_map: Dict[str, Any], timestamp_class=ts.AtmotubeTimestamp, postgis_class=geo.PostgisPoint):
        super(AtmotubeUniformResponseBuilder, self).__init__(measure_param_map=measure_param_map, timestamp_class=timestamp_class)
        self.postgis_class = postgis_class

    def build(self, responses: List[atm_mdl.AtmotubeAPIResponse]) -> List[baseadapt.FetchUniformResponse]:
        uniformed_responses = []
        for response in responses:
            timestamp = self.timestamp_class(timest=response.time)
            parameters = [baseadapt.ParamIDValue(id_=self.measure_param_map[p.name], value=p.value) for p in response.parameters]
            geolocation = geo.NullGeometry()
            if response.lat is not None and response.lon is not None:
                geolocation = self.postgis_class(lat=response.lat, lng=response.lon)
            uniformed_responses.append(baseadapt.FetchUniformResponse(timestamp=timestamp, parameters=parameters, geolocation=geolocation))
        return uniformed_responses
