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

    def __init__(self, fetch_wrapper: fetch.FetchWrapper):
        super(DateLooper, self).__init__()
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
    def _next_date(self) -> Dict[str, Any]:
        pass


################################ ATMOTUBE LOOPER ################################
class AtmotubeDateLooper(DateLooper):

    def __init__(self, fetch_wrapper: fetch.FetchWrapper, start_ts: ts.SQLTimestamp, stop_ts: ts.SQLTimestamp):
        super(AtmotubeDateLooper, self).__init__(fetch_wrapper)
        self.start = start_ts
        self.stop = stop_ts
        self.ended = False

    def has_next(self):
        return not self.ended

    def get_next_sensor_data(self) -> List[Dict[str, Any]]:
        next_date = self._next_date()
        self.fetch_wrapper.update_url_param(next_date)
        self.info_messages.append(f"{DateLooper.__name__} is looking for new data at '{next_date['date']}'")
        self.log_messages()
        return self.fetch_wrapper.get_sensor_data()

    def _next_date(self) -> Dict[str, Any]:
        date = self.start
        if date.is_after(self.stop) or date.is_same_day(self.stop):
            self.ended = True
            date = self.stop
        self.start = self.start.add_days(1)
        return {'date': date.ts.split(' ')[0]}


################################ THINGSPEAK LOOPER ################################
class ThingspeakDateLooper(DateLooper):

    def __init__(self, fetch_wrapper: fetch.FetchWrapper, start_ts: ts.SQLTimestamp, stop_ts: ts.SQLTimestamp):
        super(ThingspeakDateLooper, self).__init__(fetch_wrapper)
        self.start = start_ts
        self.stop = stop_ts
        self.ended = False

    def has_next(self):
        return not self.ended

    def get_next_sensor_data(self) -> List[Dict[str, Any]]:
        next_time_window = self._next_date()
        self.info_messages.append(f"{DateLooper.__name__} is looking for new data within "
                                  f"[{next_time_window['start']} - {next_time_window['end']}]")
        self.log_messages()
        self.fetch_wrapper.update_url_param(next_time_window)
        return self.fetch_wrapper.get_sensor_data()

    def _next_date(self) -> Dict[str, Any]:
        date = self.start
        end = self.start.add_days(7)
        if end.is_after(self.stop) or end.is_same_day(self.stop):
            self.ended = True
            end = self.stop
        self.start = self.start.add_days(7)
        return {'start': date.ts, 'end': end.ts}
