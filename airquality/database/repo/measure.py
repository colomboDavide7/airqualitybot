######################################################
#
# Author: Davide Colombo
# Date: 06/12/21 19:08
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict
import airquality.database.repo.abc as baserepo
import airquality.database.conn.adapt as dbadapt
import airquality.database.util.query as qry
import airquality.types.channel as chtype
import airquality.types.timestamp as tstype


# ------------------------------- MeasureLookupType ------------------------------- #
class MeasureLookupType(object):

    def __init__(self, sensor_id: int, channels: List[chtype.Channel]):
        self.sensor_id = sensor_id
        self.channels = channels


# ------------------------------- SensorMeasureRepo ------------------------------- #
class SensorMeasureRepo(baserepo.DatabaseRepoABC):

    def __init__(self, db_adapter: dbadapt.DatabaseAdapter, query_builder: qry.QueryBuilder, sensor_type: str):
        super(SensorMeasureRepo, self).__init__(db_adapter=db_adapter, query_builder=query_builder)
        self.sensor_type = sensor_type

    @property
    def measure_param(self) -> Dict[str, int]:
        meas_param_query = self.query_builder.query_file.s5.format(personality=self.sensor_type)
        db_lookup = self.db_adapter.send(meas_param_query)
        return {param_code: param_id for param_code, param_id in db_lookup}

    @property
    def max_mobile_record_id(self) -> int:
        query2exec = self.query_builder.query_file.s9
        db_lookup = self.db_adapter.send(query2exec)
        max_record_id = db_lookup[0][0]
        return 1 if max_record_id is None else (max_record_id + 1)

    @property
    def max_station_record_id(self) -> int:
        query2exec = self.query_builder.query_file.s10
        db_lookup = self.db_adapter.send(query2exec)
        max_record_id = db_lookup[0][0]
        return 1 if max_record_id is None else (max_record_id + 1)

    @property
    def mobile_measure_query(self) -> str:
        return self.query_builder.query_file.i1

    @property
    def station_measure_query(self) -> str:
        return self.query_builder.query_file.i2

    @property
    def update_channel_acquisition_query(self) -> str:
        return self.query_builder.query_file.u2

    ################################ lookup() ###############################
    def lookup(self) -> List[MeasureLookupType]:
        query2exec = self.query_builder.query_file.s12.format(type=self.sensor_type)
        db_lookup = self.db_adapter.send(query2exec)
        sensor_ids = [item[0] for item in db_lookup]
        return [MeasureLookupType(sensor_id=sensor_id, channels=self._apiparam_lookup(sensor_id)) for sensor_id in sensor_ids]

    ################################ _apiparam_lookup() ###############################
    def _apiparam_lookup(self, sensor_id: int) -> List[chtype.Channel]:
        query2exec = self.query_builder.query_file.s2.format(sensor_id=sensor_id)
        db_lookup = self.db_adapter.send(query2exec)
        return [chtype.Channel(ch_key=key, ch_id=ident, ch_name=name, last_acquisition=tstype.datetime2timestamp(datetime))
                for key, ident, name, datetime in db_lookup]
