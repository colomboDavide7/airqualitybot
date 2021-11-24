######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 17:59
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict, Any
import airquality.adapter.config as adapt_const
import airquality.logger.util.decorator as log_decorator
import airquality.database.operation.insert.insertoprt as base
import airquality.database.util.conn as connection
import airquality.database.util.query as query
import database.record.record as rec


################################ CLASS FOR MOBILE STATION ################################


class FetchMobileInsertWrapper(base.InsertWrapper):

    ################################ __init__ ################################
    def __init__(self,
                 conn: connection.DatabaseAdapter,
                 query_builder: query.QueryBuilder,
                 sensor_measure_rec: rec.MobileMeasureRecord,
                 log_filename="log"
    ):
        super(FetchMobileInsertWrapper, self).__init__(conn=conn, query_builder=query_builder, log_filename=log_filename)
        self.sensor_measure_rec = sensor_measure_rec

    ################################ insert ################################
    @log_decorator.log_decorator()
    def insert(self, sensor_data: List[Dict[str, Any]], sensor_id: int = None, sensor_channel: str = None):

        # Create measure values
        measure_values = [self.sensor_measure_rec.record(sensor_data=data) for data in sensor_data]

        # Build query
        exec_query = self.query_builder.insert_mobile_measurements(values=measure_values, sensor_id=sensor_id, channel=sensor_channel)
        self.conn.send(exec_query)

        # Log messages
        fst_rec_id = sensor_data[0][adapt_const.REC_ID]
        lst_rec_id = sensor_data[-1][adapt_const.REC_ID]
        tot = (lst_rec_id - fst_rec_id) + 1
        self.log_info(f"{FetchMobileInsertWrapper.__name__}: inserted {tot} mobile records within record_id "
                      f"[{fst_rec_id} - {lst_rec_id}]")


################################ CLASS FOR SENSOR STATION ################################


class FetchStationInsertWrapper(base.InsertWrapper):

    ################################ __init__ ################################
    def __init__(self,
                 conn: connection.DatabaseAdapter,
                 query_builder: query.QueryBuilder,
                 sensor_measure_rec: rec.StationMeasureRecord,
                 log_filename="log"
    ):
        super(FetchStationInsertWrapper, self).__init__(conn=conn, query_builder=query_builder, log_filename=log_filename)
        self.sensor_measure_rec = sensor_measure_rec

    ################################ insert ################################
    @log_decorator.log_decorator()
    def insert(self, sensor_data: List[Dict[str, Any]], sensor_id: int = None, sensor_channel: str = None):

        # Create measure values
        measure_values = [self.sensor_measure_rec.record(sensor_data=data, sensor_id=sensor_id) for data in sensor_data]

        # Build query
        exec_query = self.query_builder.insert_station_measurements(values=measure_values,
                                                                    sensor_id=sensor_id,
                                                                    channel=sensor_channel)
        self.conn.send(exec_query)

        # Log messages
        fst_rec_id = sensor_data[0][adapt_const.REC_ID]
        lst_rec_id = sensor_data[-1][adapt_const.REC_ID]
        tot = (lst_rec_id - fst_rec_id) + 1
        self.log_info(f"{FetchStationInsertWrapper.__name__}: inserted {tot} station records within record_id "
                      f"[{fst_rec_id} - {lst_rec_id}]")
