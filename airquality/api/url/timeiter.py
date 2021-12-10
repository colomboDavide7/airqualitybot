######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 20:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Tuple
import airquality.api.url.abc as urlabc
import airquality.api.url.private as privateurl
import airquality.types.timestamp as tstype


# ------------------------------- TimeIterableURLBuilderABC ------------------------------- #
class TimeIterableURLBuilderABC(urlabc.URLBuilderABC, abc.ABC):

    def __init__(self, url: privateurl.PrivateURLBuilderABC, start_ts: tstype.Timestamp, stop_ts: tstype.Timestamp, step_size_in_days: int = 1):
        self.url_obj = url
        self._start_ts = start_ts
        self._stop_ts = stop_ts
        self.step_size_in_days = step_size_in_days

    ################################ build() ################################
    def build(self) -> Tuple[str]:
        all_urls = []
        while self._stop_ts.is_after(self._start_ts):
            url_str = self.format_url()
            all_urls.append(url_str)
            self._start_ts = self._start_ts.add_days(self.step_size_in_days)
        return tuple(all_urls)

    @abc.abstractmethod
    def format_url(self) -> str:
        pass


# ------------------------------- AtmotubeTimeIterableURL ------------------------------- #
class AtmotubeTimeIterableURL(TimeIterableURLBuilderABC):

    def __init__(self, url: privateurl.AtmotubeURLBuilder, start_ts: tstype.Timestamp, stop_ts: tstype.Timestamp, step_size_in_days: int = 1):
        super(AtmotubeTimeIterableURL, self).__init__(url=url, start_ts=start_ts, stop_ts=stop_ts, step_size_in_days=step_size_in_days)

    ################################ format_url() ################################
    def format_url(self) -> str:
        date = self._start_ts.ts.split(' ')[0]
        ch_key = self.url_obj.api_key
        mac = self.url_obj.ident
        resp_fmt = self.url_obj.fmt
        return self.url_obj.url.format(api_key=ch_key, mac=mac, fmt=resp_fmt, date=date)


# ------------------------------- ThingspeakTimeIterableURL ------------------------------- #
class ThingspeakTimeIterableURL(TimeIterableURLBuilderABC):

    def __init__(self, url: privateurl.ThingspeakURLBuilder, start_ts: tstype.Timestamp, stop_ts: tstype.Timestamp, step_size_in_days: int = 7):
        super(ThingspeakTimeIterableURL, self).__init__(url=url, start_ts=start_ts, stop_ts=stop_ts, step_size_in_days=step_size_in_days)

    ################################ format_url() ################################
    def format_url(self) -> str:
        _from = self._start_ts.ts.replace(" ", "%20")
        _to = self.get_end_timestamp().ts.replace(" ", "%20")
        ch_id = self.url_obj.ident
        ch_key = self.url_obj.api_key
        resp_fmt = self.url_obj.fmt
        return self.url_obj.url.format(channel_id=ch_id, api_key=ch_key, fmt=resp_fmt, start=_from, end=_to)

    ################################ get_end_timestamp() ################################
    def get_end_timestamp(self) -> tstype.Timestamp:
        tmp_end = self._start_ts.add_days(self.step_size_in_days)
        if tmp_end.is_after(self._stop_ts):
            tmp_end = self._stop_ts
        return tmp_end
