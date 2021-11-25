######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 20:19
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.api2db.initunif.initunif as baseadapt
import airquality.api.resp.purpresp as resp
import airquality.database.ext.postgis as geo
import airquality.database.dtype.timestamp as ts
import airquality.database.op.sel.sel as sel


class PurpleairUniformResponseBuilder(baseadapt.InitUniformResponseBuilder):

    def __init__(self, timestamp_class=ts.UnixTimestamp, postgis_class=geo.PostgisPoint):
        super(PurpleairUniformResponseBuilder, self).__init__(timestamp_class=timestamp_class, postgis_class=postgis_class)

    def uniform(self, responses: List[resp.PurpAPIResp]) -> List[baseadapt.InitUniformResponse]:
        uniformed_responses = []
        for response in responses:
            # Create Name
            sensor_name = f"{response.name} ({response.sensor_index})".replace("'", "")
            sensor_type = "Purpleair/Thingspeak"

            # Channel parameters
            channel_param = [sel.ChannelParam(ch_name=c['name'],
                                              ch_key=response.data[c['key']],
                                              ch_id=response.data[c['id']],
                                              last_acquisition=self.timestamp_class(timest=response.date_created)
                                              ) for c in response.__class__.CHANNEL_PARAM]
            # Create sensor geometry
            geometry = self.postgis_class(lat=response.latitude, lng=response.longitude)
            # Create sensor geolocation
            geolocation = baseadapt.baseunif.ParamLocationTimestamp(geometry=geometry, timestamp=ts.CurrentTimestamp())

            # Append Uniformed Response
            uniformed_responses.append(
                baseadapt.InitUniformResponse(
                    sensor_name=sensor_name,
                    sensor_type=sensor_type,
                    channel_param=channel_param,
                    geolocation=geolocation
                )
            )

        return uniformed_responses
