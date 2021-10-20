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
    def select_all_sensor_ids_by_model(models: List[str]) -> str:
        """Static method that returns the query for getting the sensor ids
        based on model name.

        If model name is 'Atmotube Pro', then the ids are searched within the
        mobile data schema, otherwise within the station data schema."""

        base_query = """SELECT s.id 
                        FROM {schema1}.{sens_t} AS s 
                        INNER JOIN {schema2}.{man_info_t} AS m 
                        ON s.manufacturer_id = m.id
                        WHERE m.model_name = '{mod_name}';"""

        to_execute = ""
        for model_name in models:
            if model_name == 'Atmotube Pro':
                to_execute += base_query.format(schema1=LEVEL0_MOBILE_SCHEMA,
                                                sens_t=SENSOR_TABLE,
                                                schema2=LEVEL0_MOBILE_SCHEMA,
                                                man_info_t=MANUFACTURER_INFO_TABLE,
                                                mod_name=model_name)
            elif model_name == 'PurpleAir PA-II':
                to_execute += base_query.format(schema1 = LEVEL0_STATION_SCHEMA,
                                                sens_t = SENSOR_TABLE,
                                                schema2 = LEVEL0_STATION_SCHEMA,
                                                man_info_t = MANUFACTURER_INFO_TABLE,
                                                mod_name = model_name)
            else:
                raise SystemExit(f"{SQLQueryBuilder.__name__}: "
                                 f"invalid model name '{model_name}' in "
                                 f"'{SQLQueryBuilder.select_all_sensor_ids_by_model.__name__}()'")

        return to_execute
