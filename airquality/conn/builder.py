#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 10:29
# @Description: This script contains a class that defines methods for getting
#               queries
#
#################################################
import builtins


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
    def select_all_sensor_ids_by_model(model_name: str) -> str:
        """Static method that returns the query for getting the sensor ids
        based on model name.

        If model name is 'Atmotube Pro', then the ids are searched within the
        mobile data schema, otherwise within the station data schema."""

        if model_name == 'Atmotube Pro':
            schema = LEVEL0_MOBILE_SCHEMA
        elif model_name == 'PurpleAir PA-II':
            schema = LEVEL0_STATION_SCHEMA
        else:
            raise SystemExit(f"{SQLQueryBuilder.__name__}: "
                             f"invalid model name '{model_name}' in "
                             f"'{SQLQueryBuilder.select_all_sensor_ids_by_model.__name__}()'")

        return f"""SELECT s.id 
                FROM {schema}.{SENSOR_TABLE} AS s 
                INNER JOIN {schema}.{MANUFACTURER_INFO_TABLE} AS m 
                ON s.manufacturer_id = m.id
                WHERE m.model_name = '{model_name}';"""
