######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 20:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.api.url.dynurl as dyn
import airquality.database.dtype.timestamp as ts


############################# TIME URL DECORATOR BASE CLASS ##############################
class URLTimeDecorator(dyn.DynamicURLBuilder, abc.ABC):

    def __init__(self, target: dyn.DynamicURLBuilder, step_size_in_days: int = 1):
        super(URLTimeDecorator, self).__init__(address=target.address, options=target.options)
        self.target = target
        self.step_size_in_days = step_size_in_days
        self.start_ts: ts.SQLTimestamp = ts.CurrentTimestamp()
        self.stop_ts: ts.SQLTimestamp = ts.CurrentTimestamp()
        self.ended = False

    def with_start_ts(self, start: ts.SQLTimestamp):
        self.start_ts = start
        return self

    def with_stop_ts(self, stop: ts.SQLTimestamp):
        self.stop_ts = stop
        return self

    @abc.abstractmethod
    def get_next_date(self):
        pass

    def has_next_date(self):
        return not self.ended


############################# ATMOTUBE TIME URL DECORATOR ##############################
class AtmotubeURLTimeDecorator(URLTimeDecorator):

    def __init__(self, target: dyn.AtmotubeURLBuilder, step_size_in_days: int = 1):
        super(AtmotubeURLTimeDecorator, self).__init__(target=target, step_size_in_days=step_size_in_days)
        self.date: str = ""

    def build(self) -> str:
        self.get_next_date()
        basic_url = self.target.build()
        basic_url += f"&date={self.date}"
        return basic_url

    def get_next_date(self):
        current_date = self.start_ts
        if current_date.is_after(self.stop_ts) or current_date.is_same_day(self.stop_ts):
            self.ended = True
            current_date = self.stop_ts

        self.start_ts = self.start_ts.add_days(self.step_size_in_days)
        self.date = current_date.get_formatted_timestamp().split(' ')[0]


############################# THINGSPEAK TIME URL DECORATOR ##############################
class ThingspeakURLTimeDecorator(URLTimeDecorator):

    def __init__(self, target: dyn.ThingspeakURLBuilder, step_size_in_days: int = 7):
        super(ThingspeakURLTimeDecorator, self).__init__(target=target, step_size_in_days=step_size_in_days)
        self.start: str = ""
        self.end: str = ""

    def build(self) -> str:
        self.get_next_date()
        basic_url = self.target.build()
        basic_url += f"&start={self.start}&end={self.end}"
        return basic_url

    def get_next_date(self):
        current_start = self.start_ts
        current_end = self.start_ts.add_days(7)
        if current_end.is_after(self.stop_ts) or current_end.is_same_day(self.stop_ts):
            self.ended = True
            current_end = self.stop_ts

        self.start_ts = self.start_ts.add_days(self.step_size_in_days)
        self.start = current_start.get_formatted_timestamp().replace(" ", "%20")
        self.end = current_end.get_formatted_timestamp().replace(" ", "%20")
