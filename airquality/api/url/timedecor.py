######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 20:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.api.url.dynurl as dyn
import airquality.types.timestamp as ts


############################# TIME URL DECORATOR BASE CLASS ##############################
class URLTimeDecorator(dyn.DynamicURLBuilder, abc.ABC):

    def __init__(self, to_decorate: dyn.DynamicURLBuilder, step_size_in_days: int = 1):
        super(URLTimeDecorator, self).__init__(url_template=to_decorate.url_template)
        self._url_to_decorate = to_decorate
        self.step_size_in_days = step_size_in_days
        self._start: ts.SQLTimestamp = ts.NullTimestamp()
        self._stop: ts.SQLTimestamp = ts.NullTimestamp()
        self._ended = False

    def with_identifier(self, ident: str):
        self._url_to_decorate.with_identifier(ident)
        return self

    def with_api_key(self, api_key: str):
        self._url_to_decorate.with_api_key(api_key)
        return self

    def from_(self, start: ts.SQLTimestamp):
        self._start = start
        return self

    def to_(self, stop: ts.SQLTimestamp):
        self._stop = stop
        return self

    def can_start_again(self):
        self._ended = False
        return self

    @abc.abstractmethod
    def get_next_date(self):
        pass

    def has_next_date(self):
        return not self._ended


############################# ATMOTUBE TIME URL DECORATOR ##############################
class AtmotubeURLTimeDecorator(URLTimeDecorator):

    def __init__(self, to_decorate: dyn.AtmotubeURLBuilder, step_size_in_days: int = 1):
        super(AtmotubeURLTimeDecorator, self).__init__(to_decorate=to_decorate, step_size_in_days=step_size_in_days)
        self.date: str = ""

    def build(self) -> str:
        self.get_next_date()
        basic_url = self._url_to_decorate.build()
        basic_url += f"&date={self.date}"
        return basic_url

    def get_next_date(self):
        current_date = self._start
        if current_date.is_after(self._stop) or current_date.is_same_day(self._stop):
            self._ended = True
            current_date = self._stop

        self._start = self._start.add_days(self.step_size_in_days)
        self.date = current_date.get_formatted_timestamp().split(' ')[0]


############################# THINGSPEAK TIME URL DECORATOR ##############################
class ThingspeakURLTimeDecorator(URLTimeDecorator):

    def __init__(self, to_decorate: dyn.ThingspeakURLBuilder, step_size_in_days: int = 7):
        super(ThingspeakURLTimeDecorator, self).__init__(to_decorate=to_decorate, step_size_in_days=step_size_in_days)
        self.start_url_param: str = ""
        self.end_url_param: str = ""

    def build(self) -> str:
        self.get_next_date()
        basic_url = self._url_to_decorate.build()
        basic_url += f"&start={self.start_url_param}&end={self.end_url_param}"
        return basic_url

    def get_next_date(self):
        current_start = self._start
        current_end = self._start.add_days(7)
        if current_end.is_after(self._stop) or current_end.is_same_day(self._stop):
            self._ended = True
            current_end = self._stop

        self._start = self._start.add_days(self.step_size_in_days)
        self.start_url_param = current_start.get_formatted_timestamp().replace(" ", "%20")
        self.end_url_param = current_end.get_formatted_timestamp().replace(" ", "%20")
