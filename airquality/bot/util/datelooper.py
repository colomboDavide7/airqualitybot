######################################################
#
# Author: Davide Colombo
# Date: 14/11/21 16:40
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict, Any
import airquality.logger.loggable as log
import airquality.logger.util.decorator as log_decorator
import airquality.api.fetch as fetch
import airquality.database.util.datatype.timestamp as ts


def get_date_looper_class(sensor_type: str):

    if sensor_type == 'atmotube':
        return AtmotubeDateLooper
    elif sensor_type == 'thingspeak':
        return ThingspeakDateLooper
    else:
        raise SystemExit(f"'{get_date_looper_class.__name__}()': bad type => '{DateLooper.__name__}' undefined "
                         f"for sensor_type='{sensor_type}'")


################################ DATE LOOPER ################################
class DateLooper(log.Loggable):

    def __init__(self, fetch_wrapper: fetch.FetchWrapper, log_filename="app"):
        super(DateLooper, self).__init__(log_filename=log_filename)
        self.fetch_wrapper = fetch_wrapper

    def update_url_param(self, param2update: Dict[str, Any]):
        self.fetch_wrapper.update_url_param(param2update)

    def set_channel_name(self, channel_name: str):
        self.fetch_wrapper.set_channel_name(channel_name)

    @abc.abstractmethod
    def has_next(self) -> bool:
        pass

    @abc.abstractmethod
    def get_next_sensor_data(self) -> List[Dict[str, Any]]:
        pass

    @abc.abstractmethod
    def _get_next_date_url_param(self) -> Dict[str, Any]:
        pass


################################ ATMOTUBE LOOPER ################################
class AtmotubeDateLooper(DateLooper):

    def __init__(self, fetch_wrapper: fetch.FetchWrapper, start_ts: ts.SQLTimestamp, stop_ts: ts.SQLTimestamp, log_filename="app"):
        super(AtmotubeDateLooper, self).__init__(fetch_wrapper=fetch_wrapper, log_filename=log_filename)
        self.start = start_ts
        self.stop = stop_ts
        self.ended = False

    def has_next(self):
        return not self.ended

    @log_decorator.log_decorator()
    def get_next_sensor_data(self) -> List[Dict[str, Any]]:
        next_date = self._get_next_date_url_param()
        self.log_info(f"{AtmotubeDateLooper.__name__}: looking for new sensor data on date='{next_date['date']}'")
        self.fetch_wrapper.update_url_param(next_date)
        return self.fetch_wrapper.get_sensor_data()

    def _get_next_date_url_param(self) -> Dict[str, Any]:
        date = self.start
        if date.is_after(self.stop) or date.is_same_day(self.stop):
            self.ended = True
            date = self.stop
        self.start = self.start.add_days(1)
        return {'date': date.ts.split(' ')[0]}


################################ THINGSPEAK LOOPER ################################
class ThingspeakDateLooper(DateLooper):

    def __init__(self, fetch_wrapper: fetch.FetchWrapper, start_ts: ts.SQLTimestamp, stop_ts: ts.SQLTimestamp, log_filename="app"):
        super(ThingspeakDateLooper, self).__init__(fetch_wrapper=fetch_wrapper, log_filename=log_filename)
        self.start = start_ts
        self.stop = stop_ts
        self.ended = False

    def has_next(self):
        return not self.ended

    @log_decorator.log_decorator()
    def get_next_sensor_data(self) -> List[Dict[str, Any]]:
        next_time_window = self._get_next_date_url_param()
        self.log_info(f"{ThingspeakDateLooper.__name__}: looking for new measurements within date range "
                      f"[{next_time_window['start']} - {next_time_window['end']}]")
        self.fetch_wrapper.update_url_param(next_time_window)
        return self.fetch_wrapper.get_sensor_data()

    def _get_next_date_url_param(self) -> Dict[str, Any]:
        date = self.start
        end = self.start.add_days(7)
        if end.is_after(self.stop) or end.is_same_day(self.stop):
            self.ended = True
            end = self.stop
        self.start = self.start.add_days(7)
        return {'start': date.ts, 'end': end.ts}
