######################################################
#
# Author: Davide Colombo
# Date: 24/11/21 10:03
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.api.resp.purpresp as purpmdl
import database.postgis.geom as geo
import airquality.database.datatype.timestamp as ts
import airquality.api2db.updtunif.updtunif as baseupdt


class PurpleairUniformResponseBuilders(baseupdt.UpdateUniformResponseBuilder):

    def __init__(self, timestamp_class=ts.Timestamp, postgis_class=geo.PostgisPoint):
        super(PurpleairUniformResponseBuilders, self).__init__(timestamp_class=timestamp_class, postgis_class=postgis_class)

    def build(self, responses: List[purpmdl.PurpleairAPIResponse]) -> List[baseupdt.UpdateUniformResponse]:
        uniformed_responses = []
        for response in responses:
            geometry = self.postgis_class(lat=response.latitude, lng=response.longitude)
            geolocation = baseupdt.base.ParamLocationTimestamp(geolocation=geometry, timestamp=ts.CurrentTimestamp())
            uniformed_responses.append(baseupdt.UpdateUniformResponse(geolocation=geolocation))
        return uniformed_responses
