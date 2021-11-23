######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 20:00
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import airquality.api.model.thnkresp as thk_mdl
import airquality.database.util.datatype.timestamp as ts
import airquality.adapter.api2db.fetchadapt.fetchadapt as baseadapt


class ThingspeakFetchAPI2DBAdapter(baseadapt.FetchAPI2DBAdapter):

    def __init__(self, measure_param_map: Dict[str, Any], timestamp_class=ts.ThingspeakTimestamp):
        super(ThingspeakFetchAPI2DBAdapter, self).__init__(measure_param_map=measure_param_map, timestamp_class=timestamp_class)

    def adapt(self, responses: List[thk_mdl.RESP_MODEL_TYPE]) -> List[baseadapt.FetchUniformModel]:
        uniformed_responses = []
        for response in responses:
            timestamp = self.timestamp_class(timest=response.created_at)
            parameters = [baseadapt.ParamIDValue(id_=self.measure_param_map[p.name], value=p.value) for p in response.parameters]
            uniformed_responses.append(baseadapt.FetchUniformModel(timestamp=timestamp, parameters=parameters))
        return uniformed_responses
