######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 20:19
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.api2db.initunif.initunif as baseadapt
import airquality.api.resp.purpresp as purpmdl
import airquality.database.ext.postgis as geo
import airquality.database.dtype.timestamp as ts


class PurpleairUniformResponseBuilder(baseadapt.InitUniformResponseBuilder):

    def __init__(self, timestamp_class=ts.UnixTimestamp, postgis_class=geo.PostgisPoint):
        super(PurpleairUniformResponseBuilder, self).__init__(timestamp_class=timestamp_class, postgis_class=postgis_class)

    def uniform(self, responses: List[purpmdl.PurpleairResponse]) -> List[baseadapt.InitUniformResponse]:
        uniformed_responses = []
        for response in responses:
            # Create Name
            name = f"{response.name} ({response.sensor_index})".replace("'", "")
            type_ = "Purpleair/Thingspeak"

            # Create channel info List
            channels = [baseadapt.base.ParamNameTimestamp(name=ch, timestamp=self.timestamp_class(timest=response.date_created))
                        for ch in response.CHANNELS]

            # Create sensor geometry
            geometry = self.postgis_class(lat=response.latitude, lng=response.longitude)
            # Create sensor geolocation
            geolocation = baseadapt.base.ParamLocationTimestamp(geometry=geometry, timestamp=ts.CurrentTimestamp())

            # Append Uniformed Model
            uniformed_responses.append(
                baseadapt.InitUniformResponse(
                    name=name, type_=type_,
                    parameters=response.parameters,
                    channels=channels,
                    geolocation=geolocation
                )
            )

        return uniformed_responses
