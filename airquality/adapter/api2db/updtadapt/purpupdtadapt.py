######################################################
#
# Author: Davide Colombo
# Date: 24/11/21 10:03
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.api.model.purpresp as purpmdl
import airquality.database.util.postgis.geom as geo
import airquality.database.util.datatype.timestamp as ts
import airquality.adapter.api2db.updtadapt.updtadapt as baseupdt


class PurpleairUpdateAdapter(baseupdt.UpdateAPI2DBAdapter):

    def __init__(self, timestamp_class=ts.Timestamp, postgis_class=geo.PostgisPoint):
        super(PurpleairUpdateAdapter, self).__init__(timestamp_class=timestamp_class, postgis_class=postgis_class)

    def adapt(self, responses: List[purpmdl.PurpleairAPIResponseModel]) -> List[baseupdt.UpdateUniformModel]:
        uniformed_responses = []
        for response in responses:
            geometry = self.postgis_class(lat=response.latitude, lng=response.longitude)
            geolocation = baseupdt.base.ParamLocationTimestamp(geolocation=geometry, timestamp=ts.CurrentTimestamp())
            uniformed_responses.append(baseupdt.UpdateUniformModel(geolocation=geolocation))
        return uniformed_responses
