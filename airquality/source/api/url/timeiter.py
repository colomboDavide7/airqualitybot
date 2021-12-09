######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 20:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Generator
import source.api.url.private as dyn
import airquality.types.timestamp as tstype


############################# TIME URL DECORATOR BASE CLASS ##############################
class TimeIterableURL(dyn.PrivateURL, abc.ABC):

    def __init__(self, url_template: str, step_size_in_days: int = 1):
        super(TimeIterableURL, self).__init__(url_template=url_template)
        self.step_size_in_days = step_size_in_days
        self._start = tstype.NullTimestamp()
        self._stop = tstype.NullTimestamp()

    @abc.abstractmethod
    def build(self) -> Generator[str, None, None]:
        pass

    def with_identifier(self, ident: str):
        self.ident = ident
        return self

    def with_api_key(self, api_key: str):
        self.api_key = api_key
        return self

    def from_(self, start: tstype.SQLTimestamp):
        self._start = start
        return self

    def to_(self, stop: tstype.SQLTimestamp):
        self._stop = stop
        return self

    @abc.abstractmethod
    def with_url_time_param_template(self):
        pass


############################# ATMOTUBE TIME URL DECORATOR ##############################
class AtmotubeTimeIterableURL(TimeIterableURL):

    def __init__(self, url_template: str, step_size_in_days: int = 1):
        super(AtmotubeTimeIterableURL, self).__init__(url_template=url_template, step_size_in_days=step_size_in_days)
        self.date: str = ""

    def build(self) -> Generator[str, None, None]:

        while self._stop.is_after(self._start):
            date_url_param = self._start.tstype.split(' ')[0]
            yield self.url_template.format(api_key=self.api_key, mac=self.ident, fmt=self.fmt, date=date_url_param)
            self._start = self._start.add_days(self.step_size_in_days)

    def with_url_time_param_template(self):
        self.url_template += "&date={date}"
        return self


############################# THINGSPEAK TIME URL DECORATOR ##############################
class ThingspeakTimeIterableURL(TimeIterableURL):

    def __init__(self, url_template: str, step_size_in_days: int = 7):
        super(ThingspeakTimeIterableURL, self).__init__(url_template=url_template, step_size_in_days=step_size_in_days)
        self.start_url_param: str = ""
        self.end_url_param: str = ""

    def build(self) -> Generator[str, None, None]:

        while self._stop.is_after(self._start):
            start_param = self._start.tstype.replace(" ", "%20")
            tmp_end = self._start.add_days(self.step_size_in_days)
            if tmp_end.is_after(self._stop):
                tmp_end = self._stop
            end_param = tmp_end.ts.replace(" ", "%20")
            yield self.url_template.format(channel_id=self.ident, api_key=self.api_key, fmt=self.fmt, start=start_param, end=end_param)
            self._start = self._start.add_days(self.step_size_in_days)

    def with_url_time_param_template(self):
        self.url_template += "&start={start}&end={end}"
        return self
