######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 20:00
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import airquality.api.resp.thnkresp as thk_mdl
import airquality.database.dtype.timestamp as ts
import airquality.api2db.fetchunif.fetchunif as baseadapt


class ThingspeakUniformResponseBuilder(baseadapt.FetchUniformResponseBuilder):

    def __init__(self, measure_param_map: Dict[str, Any], timestamp_class=ts.ThingspeakTimestamp):
        super(ThingspeakUniformResponseBuilder, self).__init__(measure_param_map=measure_param_map, timestamp_class=timestamp_class)

    def uniform(self, responses: List[thk_mdl.RESP_TYPE]) -> List[baseadapt.FetchUniformResponse]:
        uniformed_responses = []
        for response in responses:
            timestamp = self.timestamp_class(timest=response.created_at)
            parameters = [baseadapt.ParamIDValue(id_=self.measure_param_map[p.sensor_name], value=p.value) for p in response.measures]
            uniformed_responses.append(baseadapt.FetchUniformResponse(timestamp=timestamp, parameters=parameters))
        return uniformed_responses
