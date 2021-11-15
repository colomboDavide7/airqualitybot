######################################################
#
# Author: Davide Colombo
# Date: 14/11/21 16:40
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.api.util.url as url
import airquality.database.util.datatype.timestamp as ts


def get_date_looper_class(sensor_type: str):

    if sensor_type == 'atmotube':
        return AtmotubeDateLooper
    elif sensor_type == 'thingspeak':
        return ThingspeakDateLooper
    else:
        raise SystemExit(f"'{get_date_looper_class.__name__}()': "
                         f"bad type => {DateLooper.__name__} undefined for type '{sensor_type}'")


class DateLooper(abc.ABC):

    @abc.abstractmethod
    def has_next(self) -> bool:
        pass

    @abc.abstractmethod
    def get_next_url(self) -> str:
        pass


class AtmotubeDateLooper(DateLooper):

    def __init__(self, url_builder: url.URLBuilder, start_ts: ts.SQLTimestamp, stop_ts: ts.SQLTimestamp):
        self.start = start_ts
        self.stop = stop_ts
        self.builder = url_builder
        self.ended = False

    def has_next(self):
        return not self.ended

    def get_next_url(self) -> str:
        if self.has_next():

            date = self.start
            if date.is_after(self.stop):
                self.ended = True
                date = self.stop

            next_date = {'date': date.ts.split(' ')[0]}
            self.builder.url_param.update(next_date)
            self.start = self.start.add_days(1)
            return self.builder.url()


class ThingspeakDateLooper(DateLooper):

    def __init__(self, url_builder: url.URLBuilder, start_ts: ts.SQLTimestamp, stop_ts: ts.SQLTimestamp):
        self.start = start_ts
        self.stop = stop_ts
        self.builder = url_builder
        self.ended = False

    def has_next(self):
        return not self.ended

    def get_next_url(self) -> str:
        if self.has_next():

            end = self.start.add_days(7)
            if end.is_after(self.stop):
                self.ended = True
                end = self.stop

            next_start = {'start': self.start.ts.replace(" ", "%20"), 'end': end.ts.replace(" ", "%20")}
            self.builder.url_param.update(next_start)
            self.start = self.start.add_days(7)
            return self.builder.url()
