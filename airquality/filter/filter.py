######################################################
#
# Author: Davide Colombo
# Date: 14/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict, Any
import airquality.logger.loggable as log
import airquality.database.util.datatype.timestamp as ts
import airquality.database.operation.select.type as sel_type
import airquality.adapter.config as adapt_const


def get_sensor_data_filter(bot_name: str, sel_wrapper: sel_type.TypeSelectWrapper):

    if bot_name == 'init':
        database_sensor_names = sel_wrapper.get_sensor_names()
        return NameFilter(database_sensor_names=database_sensor_names)
    elif bot_name == 'update':
        active_locations = sel_wrapper.get_active_locations()
        return GeoFilter(database_active_locations=active_locations)
    elif bot_name == 'fetch':
        return TimestampFilter()
    else:
        raise SystemExit(f"'{get_sensor_data_filter.__name__}():' bad name '{bot_name}'")


################################ SENSOR DATA FILTER BASE CLASS ################################
class SensorDataFilter(log.Loggable):

    @abc.abstractmethod
    def filter(self, sensor_data: Dict[str, Any]) -> bool:
        pass


################################ NAME FILTER ################################
class NameFilter(SensorDataFilter):

    def __init__(self, database_sensor_names: List[str]):
        super(NameFilter, self).__init__()
        self.database_sensor_names = database_sensor_names

    def filter(self, sensor_data: Dict[str, Any]) -> bool:
        return sensor_data[adapt_const.SENS_NAME] not in self.database_sensor_names


################################ TIMESTAMP FILTER ################################
class TimestampFilter(SensorDataFilter):

    def __init__(self):
        super(TimestampFilter, self).__init__()
        self.filter_ts = None

    def set_filter_ts(self, filter_ts=ts.SQLTimestamp):
        self.filter_ts = filter_ts

    def filter(self, sensor_data: Dict[str, Any]) -> bool:

        if not self.filter_ts:
            raise SystemExit(f"{TimestampFilter.__name__}: bad setup => missing external dependency 'filter_ts'")

        timestamp_class = sensor_data[adapt_const.TIMEST][adapt_const.CLS]
        class_kwargs = sensor_data[adapt_const.TIMEST][adapt_const.KW]
        timest = timestamp_class(**class_kwargs)
        return timest.is_after(self.filter_ts)


################################ GEO FILTER ################################
class GeoFilter(SensorDataFilter):

    def __init__(self, database_active_locations: Dict[str, Any]):
        super(GeoFilter, self).__init__()
        self.database_active_locations = database_active_locations

    def filter(self, sensor_data: Dict[str, Any]) -> bool:

        if sensor_data['name'] in self.database_active_locations:
            self._exit_on_bad_sensor_data(sensor_data=sensor_data)
            postgis_class = sensor_data[adapt_const.SENS_GEOM][adapt_const.CLS]
            class_kwargs = sensor_data[adapt_const.SENS_GEOM][adapt_const.KW]
            as_text = postgis_class(**class_kwargs).as_text()
            return as_text != self.database_active_locations[sensor_data['name']]
        return False

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        msg = f"{GeoFilter.__name__} bad sensor data =>"
        if adapt_const.SENS_GEOM not in sensor_data:
            raise SystemExit(f"{msg} missing key='{adapt_const.SENS_GEOM}'")
        if not sensor_data[adapt_const.SENS_GEOM]:
            raise SystemExit(f"{msg} '{adapt_const.SENS_GEOM}' cannot be empty")
        if adapt_const.CLS not in sensor_data[adapt_const.SENS_GEOM] or adapt_const.KW not in sensor_data[adapt_const.SENS_GEOM]:
            raise SystemExit(f"{msg} '{adapt_const.SENS_GEOM}' must have '{adapt_const.CLS}' and '{adapt_const.KW}' keys")
