######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 12:24
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.api2db.adptype as adptype
import airquality.api2db.adpt as adpt
import airquality.api.resp.resp as resp
import airquality.database.ext.postgis as pgis
import airquality.database.dtype.timestamp as ts
import airquality.database.op.sel.sel as sel


class AtmoAPIRespAdapt(adpt.APIRespAdapt):

    def __init__(self, measure_id_name: List[sel.ParamNameID], timestamp_cls=ts.AtmotubeTimestamp, postgis_cls=pgis.PostgisPoint):
        self.timestamp_cls = timestamp_cls
        self.postgis_cls = postgis_cls
        self.measure_id_name = measure_id_name

    def adapt(self, api_resp: List[resp.AtmoAPIResp]) -> List[adptype.MobileMeasure]:
        adapted_resp = []
        for r in api_resp:
            adapted_resp.append(
                adptype.MobileMeasure(
                    measures=self._get_measures(r),
                    geometry=self.postgis_cls(lat=r.lat, lng=r.lon),
                    timestamp=self.timestamp_cls(r.time)
                )
            )
        return adapted_resp

    def _get_measures(self, r: resp.AtmoAPIResp) -> List[adptype.ParamIDName]:
        measure_dict = {}
        for m in self.measure_id_name:
            measure_dict[m.name] = m.id
        return [adptype.ParamIDName(id_=measure_dict[m.name], value=m.value) for m in r.measures]
