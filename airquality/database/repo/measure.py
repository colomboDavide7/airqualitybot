######################################################
#
# Author: Davide Colombo
# Date: 06/12/21 19:08
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict
import airquality.database.repo.repo as baserepo
import airquality.database.conn.adapt as adapt
import airquality.database.util.query as qry
import airquality.types.channel as chtype
import airquality.types.timestamp as tstype
import airquality.types.lookup.lookup as lookuptype


################################ SENSOR MEASURE REPO ABC ###############################
class SensorMeasureRepoABC(baserepo.DatabaseRepoABC, abc.ABC):

    def __init__(self, db_adapter: adapt.DatabaseAdapter, query_builder: qry.QueryBuilder, sensor_type: str):
        super(SensorMeasureRepoABC, self).__init__(db_adapter=db_adapter, query_builder=query_builder)
        self.sensor_type = sensor_type

    @abc.abstractmethod
    def max_record_id_lookup(self) -> int:
        pass

    def apiparam_lookup(self, sensor_id: int) -> List[chtype.Channel]:
        query2exec = self.query_builder.select_api_param_from_sensor_id(sensor_id)
        db_lookup = self.db_adapter.send(query2exec)
        return [chtype.Channel(ch_key=key, ch_id=ident, ch_name=name, last_acquisition=tstype.datetime2timestamp(datetime))
                for key, ident, name, datetime in db_lookup]

    def measureparam_lookup(self) -> Dict[str, int]:
        meas_param_query = self.query_builder.select_measure_param_from_sensor_type(self.sensor_type)
        db_lookup = self.db_adapter.send(meas_param_query)
        return {param_code: param_id for param_code, param_id in db_lookup}


################################ MOBILE MEASURE REPO ###############################
class MobileMeasureRepo(SensorMeasureRepoABC):

    def __init__(self, db_adapter: adapt.DatabaseAdapter, query_builder: qry.QueryBuilder, sensor_type: str):
        super(MobileMeasureRepo, self).__init__(db_adapter=db_adapter, query_builder=query_builder, sensor_type=sensor_type)

    def lookup(self) -> List[lookuptype.SensorMeasureLookup]:
        query2exec = self.query_builder.select_sensor_id_from_type(self.sensor_type)
        db_lookup = self.db_adapter.send(query2exec)
        return [lookuptype.SensorMeasureLookup(sensor_id=sensor_id, channels=self.apiparam_lookup(sensor_id))
                for sensor_id in db_lookup]

    def push(self, responses) -> None:
        pass

    def max_record_id_lookup(self) -> int:
        query2exec = self.query_builder.select_max_mobile_record_id()
        db_lookup = self.db_adapter.send(query2exec)
        max_record_id = db_lookup[0][0]
        return 1 if max_record_id is None else (max_record_id+1)


################################ STATION MEASURE REPO ###############################
class StationMeasureRepo(SensorMeasureRepoABC):

    def __init__(self, db_adapter: adapt.DatabaseAdapter, query_builder: qry.QueryBuilder, sensor_type: str):
        super(StationMeasureRepo, self).__init__(db_adapter=db_adapter, query_builder=query_builder, sensor_type=sensor_type)

    def lookup(self) -> List[lookuptype.SensorMeasureLookup]:
        query2exec = self.query_builder.select_sensor_id_from_type(self.sensor_type)
        db_lookup = self.db_adapter.send(query2exec)
        return [lookuptype.SensorMeasureLookup(sensor_id=sensor_id, channels=self.apiparam_lookup(sensor_id))
                for sensor_id in db_lookup]

    def push(self, responses) -> None:
        pass

    def max_record_id_lookup(self) -> int:
        query2exec = self.query_builder.select_max_station_record_id()
        db_lookup = self.db_adapter.send(query2exec)
        max_record_id = db_lookup[0][0]
        return 1 if max_record_id is None else (max_record_id + 1)
