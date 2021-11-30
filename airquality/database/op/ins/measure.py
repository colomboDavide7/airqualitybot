######################################################
#
# Author: Davide Colombo
# Date: 26/11/21 12:38
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict, Any
import airquality.database.op.ins.base as base
import airquality.logger.util.decorator as log_decorator
import airquality.database.rec.measure as rec
import airquality.database.conn.adapt as db
import airquality.database.util.query as qry
import airquality.types.apiresp.measresp as resp


class MeasureInsertWrapper(base.InsertWrapper, abc.ABC):

    def __init__(
            self, conn: db.DatabaseAdapter, builder: qry.QueryBuilder, record_builder: rec.MeasureRecordBuilder, log_filename="log"
    ):
        super(MeasureInsertWrapper, self).__init__(
            conn=conn, builder=builder, record_builder=record_builder, log_filename=log_filename)
        self.record_builder = record_builder
        self.sensor_id = None
        self.record_id = None
        self.channel_name = None

    @abc.abstractmethod
    def get_measure_values(self, api_responses: List[resp.MeasureAPIResp]) -> str:
        pass

    @log_decorator.log_decorator()
    def get_update_last_acquisition_timestamp_query(self, last_response: resp.MeasureAPIResp) -> str:
        return self.query_builder.build_update_last_channel_acquisition_query(
            sensor_id=self.sensor_id,
            channel_name=self.channel_name,
            last_timestamp=last_response.timestamp.get_formatted_timestamp()
        )

    def log_report(self, start_rec_id: int, api_responses: List[resp.MeasureAPIResp]):
        start_timestamp = api_responses[0].timestamp.get_formatted_timestamp()
        last_timestamp = api_responses[-1].timestamp.get_formatted_timestamp()
        n = len(api_responses)
        self.log_info(f"{self.__class__.__name__}: inserted {n}/{n} new measurements ")
        self.log_info(f"{self.__class__.__name__}: record_id range [{start_rec_id} - {start_rec_id+n-1}]")
        self.log_info(f"{self.__class__.__name__}: timestamp range [{start_timestamp} - {last_timestamp}]")

    def with_start_insert_record_id(self, record_id: int):
        self.record_id = record_id
        return self

    def with_measure_param_name2id(self, name2id: Dict[str, Any]):
        self.record_builder.with_measure_name2id(name2id)
        return self

    def with_sensor_id(self, sensor_id: int):
        self.sensor_id = sensor_id
        self.record_builder.with_sensor_id(sensor_id)
        return self

    def with_channel_name(self, channel_name: str):
        self.channel_name = channel_name
        return self


################################ MOBILE MEASURE INSERT WRAPPER ################################
class MobileInsertWrapper(MeasureInsertWrapper):

    def __init__(
            self, conn: db.DatabaseAdapter, builder: qry.QueryBuilder, record_builder: rec.MobileRecordBuilder, log_filename="log"
    ):
        super(MobileInsertWrapper, self).__init__(
            conn=conn, builder=builder, record_builder=record_builder, log_filename=log_filename)
        self.record_builder = record_builder

    @log_decorator.log_decorator()
    def insert(self, api_responses: List[resp.MobileSensorAPIResp]) -> None:
        start_record_id = self.record_id
        measure_values = self.get_measure_values(api_responses=api_responses)
        query = self.query_builder.build_insert_mobile_measure_query(measure_values)
        query += self.get_update_last_acquisition_timestamp_query(last_response=api_responses[-1])
        self.database_conn.send(query)
        self.log_report(start_rec_id=start_record_id, api_responses=api_responses)

    @log_decorator.log_decorator()
    def get_measure_values(self, api_responses: List[resp.MobileSensorAPIResp]) -> str:
        measure_values = ""
        for r in api_responses:
            timest = r.timestamp
            self.record_builder.with_geometry(geom=r.geometry)

            measure_values += ','.join(self.record_builder.get_measure_value(
                record_id=self.record_id, timestamp=timest, param_name=m.name, param_value=m.value
            ) for m in r.measures) + ','
            self.record_id += 1
        return measure_values.strip(',')


################################ STATION MEASURE INSERT WRAPPER ################################
class StationInsertWrapper(MeasureInsertWrapper):

    def __init__(
            self, conn: db.DatabaseAdapter, builder: qry.QueryBuilder, record_builder: rec.StationRecordBuilder, log_filename="log"
    ):
        super(StationInsertWrapper, self).__init__(
            conn=conn, builder=builder, record_builder=record_builder, log_filename=log_filename)
        self.record_builder = record_builder

    @log_decorator.log_decorator()
    def insert(self, api_responses: List[resp.MeasureAPIResp]) -> None:
        start_record_id = self.record_id
        measure_values = self.get_measure_values(api_responses=api_responses)
        query = self.query_builder.build_insert_station_measure_query(measure_values)
        query += self.get_update_last_acquisition_timestamp_query(last_response=api_responses[-1])
        self.database_conn.send(query)
        self.log_report(start_rec_id=start_record_id, api_responses=api_responses)

    @log_decorator.log_decorator()
    def get_measure_values(self, api_responses: List[resp.MeasureAPIResp]) -> str:
        measure_values = ""
        for r in api_responses:
            timest = r.timestamp
            measure_values += ','.join(self.record_builder.get_measure_value(
                record_id=self.record_id, timestamp=timest, param_name=m.name, param_value=m.value
            ) for m in r.measures) + ','
            self.record_id += 1
        return measure_values.strip(',')
