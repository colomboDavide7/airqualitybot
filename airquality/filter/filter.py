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

    def __init__(self):
        super(SensorDataFilter, self).__init__()

    @abc.abstractmethod
    def filter(self, sensor_data: Dict[str, Any]) -> bool:
        pass

    @abc.abstractmethod
    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        pass

    @abc.abstractmethod
    def _log_message(self, filter_output: bool, sensor_data: Dict[str, Any]):
        pass


################################ NAME FILTER ################################
class NameFilter(SensorDataFilter):

    def __init__(self, database_sensor_names: List[str]):
        super(NameFilter, self).__init__()
        self.database_sensor_names = database_sensor_names

    def filter(self, sensor_data: Dict[str, Any]) -> bool:

        self._exit_on_bad_sensor_data(sensor_data=sensor_data)
        is_not_in = sensor_data[adapt_const.SENS_NAME] not in self.database_sensor_names
        self._log_message(filter_output=is_not_in, sensor_data=sensor_data)

        return is_not_in

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        if adapt_const.SENS_NAME not in sensor_data:
            raise SystemExit(f"{NameFilter.__name__}: bad sensor data => missing key='{adapt_const.SENS_NAME}'")

    def _log_message(self, filter_output: bool, sensor_data: Dict[str, Any]):
        msg_header = f"{NameFilter.__name__}:"
        name = sensor_data[adapt_const.SENS_NAME]

        self.log_info(f"{msg_header} found new sensor '{name}'") \
            if filter_output else \
            self.log_warning(f"{msg_header} skip sensor '{name}' => already present")


################################ TIMESTAMP FILTER ################################
class TimestampFilter(SensorDataFilter):

    def __init__(self):
        super(TimestampFilter, self).__init__()
        self.filter_ts = None

    def set_filter_ts(self, filter_ts=ts.SQLTimestamp):
        self.filter_ts = filter_ts

    def filter(self, sensor_data: Dict[str, Any]) -> bool:
        self._exit_on_bad_sensor_data(sensor_data=sensor_data)
        timestamp_class = sensor_data[adapt_const.TIMEST][adapt_const.CLS]
        class_kwargs = sensor_data[adapt_const.TIMEST][adapt_const.KW]
        timest = timestamp_class(**class_kwargs)
        return timest.is_after(self.filter_ts)

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):

        if not self.filter_ts:
            raise SystemExit(f"{TimestampFilter.__name__}: bad setup => missing external dependency 'filter_ts'")

        msg = f"{TimestampFilter.__name__}: bad sensor data =>"

        if adapt_const.TIMEST not in sensor_data:
            raise SystemExit(f"{msg} missing key='{adapt_const.TIMEST}'")
        if not sensor_data[adapt_const.TIMEST]:
            raise SystemExit(f"{msg} '{adapt_const.TIMEST}' cannot be empty")
        if adapt_const.CLS not in sensor_data[adapt_const.TIMEST] or adapt_const.KW not in sensor_data[adapt_const.TIMEST]:
            raise SystemExit(f"{msg} '{adapt_const.TIMEST}' must have '{adapt_const.CLS}' and '{adapt_const.KW}' keys")

    def _log_message(self, filter_output: bool, sensor_data: Dict[str, Any]):
        pass


################################ GEO FILTER ################################
class GeoFilter(SensorDataFilter):

    def __init__(self, database_active_locations: Dict[str, Any]):
        super(GeoFilter, self).__init__()
        self.database_active_locations = database_active_locations

    def filter(self, sensor_data: Dict[str, Any]) -> bool:

        # If the sensor is within database active locations then I check the geolocation
        if sensor_data[adapt_const.SENS_NAME] in self.database_active_locations:
            # Check correctness of sensor data
            self._exit_on_bad_sensor_data(sensor_data=sensor_data)
            # Dynamically build geolocation class
            postgis_class = sensor_data[adapt_const.SENS_GEOM][adapt_const.CLS]
            class_kwargs = sensor_data[adapt_const.SENS_GEOM][adapt_const.KW]
            as_text = postgis_class(**class_kwargs).as_text()
            # Get the output of the filter
            is_changed = as_text != self.database_active_locations[sensor_data[adapt_const.SENS_NAME]]
            # Log message
            self._log_message(filter_output=is_changed, sensor_data=sensor_data)
            return is_changed

        self.log_warning(f"{GeoFilter.__name__}: skip sensor '{sensor_data[adapt_const.SENS_NAME]}' => inactive")
        return False

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        msg = f"{GeoFilter.__name__} bad sensor data =>"
        if adapt_const.SENS_GEOM not in sensor_data:
            raise SystemExit(f"{msg} missing key='{adapt_const.SENS_GEOM}'")
        if not sensor_data[adapt_const.SENS_GEOM]:
            raise SystemExit(f"{msg} '{adapt_const.SENS_GEOM}' cannot be empty")
        if adapt_const.CLS not in sensor_data[adapt_const.SENS_GEOM] or adapt_const.KW not in sensor_data[adapt_const.SENS_GEOM]:
            raise SystemExit(f"{msg} '{adapt_const.SENS_GEOM}' must have '{adapt_const.CLS}' and '{adapt_const.KW}' keys")

    def _log_message(self, filter_output: bool, sensor_data: Dict[str, Any]):
        name = sensor_data[adapt_const.SENS_NAME]

        if filter_output:
            self.log_info(f"{GeoFilter.__name__}: found different location for sensor '{name}'")
        else:
            self.log_warning(f"{GeoFilter.__name__}: skip sensor '{name}' => same location")
