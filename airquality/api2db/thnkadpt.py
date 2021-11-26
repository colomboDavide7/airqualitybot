######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 12:47
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.api2db.adptype as adptype
import airquality.api2db.adpt as adpt
import airquality.api.resp.resp as resp
import airquality.database.dtype.timestamp as ts
import airquality.database.op.sel.sel as sel


class ThnkAPIRespAdapt(adpt.APIRespAdapt):

    def __init__(self, measure_id_name: List[sel.ParamNameID], timestamp_cls=ts.ThingspeakTimestamp):
        self.measure_id_name = measure_id_name
        self.timestamp_cls = timestamp_cls

    def adapt(self, api_resp: List[resp.THNKRESPTYPE]) -> List[adptype.StationMeasure]:
        adapted_resp = []
        for r in api_resp:
            adapted_resp.append(
                adptype.StationMeasure(
                    timestamp=self.timestamp_cls(timest=r.created_at),
                    measures=self._get_measures(r)
                )
            )
        return adapted_resp

    def _get_measures(self, r: resp.THNKRESPTYPE) -> List[adptype.ParamIDName]:
        measure_dict = {}
        for m in self.measure_id_name:
            measure_dict[m.name] = m.id
        return [adptype.ParamIDName(id_=measure_dict[m.name], value=m.value) for m in r.measures]
