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
import airquality.api.fetch as api_op
import airquality.database.util.datatype.timestamp as ts


def get_date_looper_class(sensor_type: str):

    if sensor_type == 'atmotube':
        return AtmotubeDateLooper
    elif sensor_type == 'thingspeak':
        return ThingspeakDateLooper
    else:
        raise SystemExit(f"'{get_date_looper_class.__name__}()': bad type => '{DateLooper.__name__}' undefined "
                         f"for sensor_type='{sensor_type}'")


class DateLooper(log.Loggable):

    def __init__(self, fetch_wrapper: api_op.FetchWrapper):
        super(DateLooper, self).__init__()
        self.fetch_wrapper = fetch_wrapper

    @abc.abstractmethod
    def has_next(self) -> bool:
        pass

    @abc.abstractmethod
    def get_next_sensor_data(self) -> List[Dict[str, Any]]:
        pass


class AtmotubeDateLooper(DateLooper):

    def __init__(self, fetch_wrapper: api_op.FetchWrapper, start_ts: ts.SQLTimestamp, stop_ts: ts.SQLTimestamp):
        super(AtmotubeDateLooper, self).__init__(fetch_wrapper)
        self.start = start_ts
        self.stop = stop_ts
        self.ended = False

    def has_next(self):
        return not self.ended

    def get_next_sensor_data(self) -> List[Dict[str, Any]]:
        if self.has_next():

            date = self.start
            if date.is_after(self.stop):
                self.ended = True
                date = self.stop

            next_date = {'date': date.ts.split(' ')[0]}
            self.fetch_wrapper.update_param(next_date)
            self.start = self.start.add_days(1)
            return self.fetch_wrapper.get_sensor_data()


class ThingspeakDateLooper(DateLooper):

    def __init__(self, fetch_wrapper: api_op.FetchWrapper, start_ts: ts.SQLTimestamp, stop_ts: ts.SQLTimestamp):
        super(ThingspeakDateLooper, self).__init__(fetch_wrapper)
        self.start = start_ts
        self.stop = stop_ts
        self.ended = False

    def has_next(self):
        return not self.ended

    def get_next_sensor_data(self) -> List[Dict[str, Any]]:
        if self.has_next():

            end = self.start.add_days(7)
            if end.is_after(self.stop):
                self.ended = True
                end = self.stop

            next_start = {'start': self.start.ts.replace(" ", "%20"), 'end': end.ts.replace(" ", "%20")}
            self.fetch_wrapper.update_param(next_start)
            self.start = self.start.add_days(7)
            return self.fetch_wrapper.get_sensor_data()
