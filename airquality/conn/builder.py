#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 10:29
# @Description: This script contains a class that defines methods for getting
#               queries
#
#################################################
import builtins
from typing import List

LEVEL0_STATION_SCHEMA = "level0_station_data"
LEVEL0_MOBILE_SCHEMA = "level0_mobile_data"

MANUFACTURER_INFO_TABLE = "manufacturer_info"
MEASURE_PARAM_TABLE = "measure_param"
MEASUREMENT_TABLE = "measurement"
TRACE_POINT_TABLE = "trace_point"
API_PARAM_TABLE = "api_param"
GEO_AREA_TABLE = "geo_area"
SENSOR_TABLE = "sensor"


class SQLQueryBuilder(builtins.object):
    """
    Class that defines @staticmethods for building queries in the right way.
    """

    @staticmethod
    def select_mobile_sensor_ids(models: List[str]) -> str:
        """
        Static method that builds the query for selecting the ids from
        sensor table in mobile data schema by model name."""

        if not models:
            raise SystemExit(f"{SQLQueryBuilder.__name__}: empty 'mobile' model list in "
                             f"'{SQLQueryBuilder.select_mobile_sensor_ids.__name__}()'. "
                             f"Please check your resource file.")

        query = ""
        for model in models:
            query += f"SELECT s.id FROM {LEVEL0_MOBILE_SCHEMA}.{SENSOR_TABLE} AS s " \
                    f"INNER JOIN {LEVEL0_MOBILE_SCHEMA}.{MANUFACTURER_INFO_TABLE} AS m " \
                    f"ON m.id = s.manufacturer_id " \
                    f"WHERE m.model_name = '{model}'; "

        return query
