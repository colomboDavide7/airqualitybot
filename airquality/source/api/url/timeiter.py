######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 20:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Generator
import airquality.source.api.url.abc as urlabc
import airquality.source.api.url.private as privateurl
import airquality.types.timestamp as tstype


# ------------------------------- TimeIterableURLBuilderABC ------------------------------- #
class TimeIterableURLBuilderABC(urlabc.URLBuilderABC, abc.ABC):

    def __init__(self, url: privateurl.PrivateURLBuilderABC, start_ts: tstype.Timestamp, stop_ts: tstype.Timestamp, step_size_in_days: int = 1):
        super(TimeIterableURLBuilderABC, self).__init__(url_template=url.url_template)
        self.url = url
        self._start_ts = start_ts
        self._stop_ts = stop_ts
        self.step_size_in_days = step_size_in_days

    @abc.abstractmethod
    def build(self) -> Generator[str, None, None]:
        pass

    @abc.abstractmethod
    def with_url_time_param_template(self):
        pass


# ------------------------------- AtmotubeTimeIterableURL ------------------------------- #
class AtmotubeTimeIterableURL(TimeIterableURLBuilderABC):

    def __init__(self, url: privateurl.AtmotubeURLBuilder, start_ts: tstype.Timestamp, stop_ts: tstype.Timestamp, step_size_in_days: int = 1):
        super(AtmotubeTimeIterableURL, self).__init__(url=url, start_ts=start_ts, stop_ts=stop_ts, step_size_in_days=step_size_in_days)

    ################################ build() ################################
    def build(self) -> Generator[str, None, None]:
        while self._stop_ts.is_after(self._start_ts):
            date_url_param = self._start_ts.ts.split(' ')[0]
            yield self.url_template.format(api_key=self.url.api_key, mac=self.url.ident, fmt=self.url.fmt, date=date_url_param)
            self._start_ts = self._start_ts.add_days(self.step_size_in_days)

    ################################ with_url_time_param_template() ################################
    def with_url_time_param_template(self):
        self.url_template += "&date={date}"
        return self


# ------------------------------- ThingspeakTimeIterableURL ------------------------------- #
class ThingspeakTimeIterableURL(TimeIterableURLBuilderABC):

    def __init__(self, url: privateurl.AtmotubeURLBuilder, start_ts: tstype.Timestamp, stop_ts: tstype.Timestamp, step_size_in_days: int = 7):
        super(ThingspeakTimeIterableURL, self).__init__(url=url, start_ts=start_ts, stop_ts=stop_ts, step_size_in_days=step_size_in_days)

    ################################ build() ################################
    def build(self) -> Generator[str, None, None]:
        while self._stop_ts.is_after(self._start_ts):
            start_param = self._start_ts.ts.replace(" ", "%20")
            end_param = self.get_end_timestamp().ts.replace(" ", "%20")
            yield self.url_template.format(channel_id=self.url.ident, api_key=self.url.api_key, fmt=self.url.fmt, start=start_param, end=end_param)
            self._start_ts = self._start_ts.add_days(self.step_size_in_days)

    ################################ get_end_timestamp() ################################
    def get_end_timestamp(self):
        tmp_end = self._start_ts.add_days(self.step_size_in_days)
        if tmp_end.is_after(self._stop_ts):
            tmp_end = self._stop_ts
        return tmp_end

    ################################ with_url_time_param_template() ################################
    def with_url_time_param_template(self):
        self.url_template += "&start={start}&end={end}"
        return self
