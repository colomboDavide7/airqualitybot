######################################################
#
# Author: Davide Colombo
# Date: 22/12/21 20:42
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.measure_factory import MeasureFactory
from airquality.sqltable import SQLTable

STATION_MEASURE_COLS = ['param_id', 'sensor_id', 'param_value', 'timestamp']


class ThingspeakFactory(MeasureFactory):

    def measure_table(self) -> SQLTable:
        return SQLTable(table_name="station_measurement", pkey="id", selected_cols=STATION_MEASURE_COLS)
