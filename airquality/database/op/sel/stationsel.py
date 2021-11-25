######################################################
#
# Author: Davide Colombo
# Date: 24/11/21 14:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.database.op.sel.sel as sel
import airquality.database.util.conn as db
import airquality.database.util.query as qry
import airquality.database.ext.postgis as pgis


################################ STATION DATABASE RESPONSE ################################
class StationDBResponse(sel.BaseDBResponse):

    def __init__(self, sensor_id: int, sensor_name: str, api_param: List[sel.ChannelParam], geometry: pgis.PostgisGeometry):
        self.sensor_id = sensor_id
        self.sensor_name = sensor_name
        self.api_param = api_param
        self.geometry = geometry


################################ STATION SELECT WRAPPER ################################
class StationSelectWrapper(sel.SelectWrapper):

    def __init__(
            self, conn: db.DatabaseAdapter, builder: qry.QueryBuilder, sensor_type: str, log_filename="log",
            postgis_class=pgis.PostgisPoint
    ):
        super(StationSelectWrapper, self).__init__(conn=conn, builder=builder, sensor_type=sensor_type, log_filename=log_filename)
        self.postgis_class = postgis_class

    # ************************************ select ************************************
    def select(self) -> List[StationDBResponse]:
        responses = []

        sensor_query = self.query_builder.select_sensor_id_name_from_type(sensor_type=self.sensor_type)
        sensor_resp = self.database_conn.send(sensor_query)
        for sensor_id, sensor_name in sensor_resp:
            # Query the API param + channel info
            api_param = self._select_api_param(sensor_id=sensor_id)

            # Query the sensor location
            location_query = self.query_builder.select_location_from_sensor_id(sensor_id=sensor_id)
            location_resp = self.database_conn.send(location_query)
            geometry = self.postgis_class(lat=location_resp[0][1], lng=location_resp[0][0])

            # Make the response
            responses.append(StationDBResponse(sensor_id=sensor_id, sensor_name=sensor_name, api_param=api_param, geometry=geometry))

        return responses
