######################################################
#
# Author: Davide Colombo
# Date: 06/12/21 19:08
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import itertools
from typing import List, Dict
import airquality.database.repo.repo as baserepo
import airquality.database.conn.adapt as adapt
import airquality.database.util.query as qry
import airquality.types.channel as chtype
import airquality.types.timestamp as tstype
import airquality.types.lookup.lookup as lookuptype
import airquality.types.apiresp.measresp as resptype


################################ SENSOR MEASURE REPO ABC ###############################
class SensorMeasureRepoABC(baserepo.DatabaseRepoABC, abc.ABC):

    def __init__(self, db_adapter: adapt.DatabaseAdapter, query_builder: qry.QueryBuilder, sensor_type: str):
        super(SensorMeasureRepoABC, self).__init__(db_adapter=db_adapter, query_builder=query_builder)
        self.sensor_type = sensor_type
        self.sensor_id2push = None
        self.channel_name2push = None

    @abc.abstractmethod
    def max_record_id_lookup(self) -> int:
        pass

    @abc.abstractmethod
    def lookup(self) -> List[lookuptype.SensorMeasureLookup]:
        pass

    @abc.abstractmethod
    def push(self, responses) -> None:
        pass

    def push_to(self, sensor_id: int, channel_name: str):
        self.sensor_id2push = sensor_id
        self.channel_name2push = channel_name
        return self

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
        unfolded = [item[0] for item in db_lookup]
        return [lookuptype.SensorMeasureLookup(sensor_id=sensor_id, channels=self.apiparam_lookup(sensor_id))
                for sensor_id in unfolded]

    def push(self, responses: List[resptype.MobileSensorAPIResp]) -> None:
        if not responses:
            # self.log_info(f"{self.__class__.__name__} no new measurements to insert => continue")
            return

        code2id = self.measureparam_lookup()
        start_record_id = self.max_record_id_lookup()
        record_id_iter = itertools.count(start_record_id)

        measure_values = ""
        for response in responses:
            record_id = next(record_id_iter)
            measure_values += response.measure2sql(record_id=record_id, code2id=code2id)

        measure_query = self.query_builder.build_insert_mobile_measure_query(measure_values.strip(','))
        update_query = self.query_builder.build_update_last_channel_acquisition_query(
            sensor_id=self.sensor_id2push,
            channel_name=self.channel_name2push,
            last_timestamp=responses[-1].timestamp.ts
        )
        query2exec = measure_query + update_query
        self.db_adapter.send(query2exec)

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
        unfolded = [item[0] for item in db_lookup]
        return [lookuptype.SensorMeasureLookup(sensor_id=sensor_id, channels=self.apiparam_lookup(sensor_id))
                for sensor_id in unfolded]

    def push(self, responses: List[resptype.MeasureAPIResp]) -> None:
        code2id = self.measureparam_lookup()
        start_record_id = self.max_record_id_lookup()
        record_id_iter = itertools.count(start_record_id)

        measure_values = ""
        for response in responses:
            record_id = next(record_id_iter)
            measure_values += response.measure2sql(record_id=record_id, sensor_id=self.sensor_id2push, code2id=code2id)

        measure_query = self.query_builder.build_insert_station_measure_query(measure_values.strip(','))
        update_query = self.query_builder.build_update_last_channel_acquisition_query(
            sensor_id=self.sensor_id2push, channel_name=self.channel_name2push,
            last_timestamp=responses[-1].timestamp.ts
        )
        query2exec = measure_query + update_query
        self.db_adapter.send(query2exec)

    def max_record_id_lookup(self) -> int:
        query2exec = self.query_builder.select_max_station_record_id()
        db_lookup = self.db_adapter.send(query2exec)
        max_record_id = db_lookup[0][0]
        return 1 if max_record_id is None else (max_record_id + 1)
