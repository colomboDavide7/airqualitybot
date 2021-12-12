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
import airquality.logger.loggable as log


# ------------------------------- TimeIterableURLBuilderABC ------------------------------- #
class TimeIterableURLBuilderABC(urlabc.URLBuilderABC, log.Loggable, abc.ABC):

    def __init__(self, from_: tstype.Timestamp, to_: tstype.Timestamp, step_size_in_days: int = 1):
        super(TimeIterableURLBuilderABC, self).__init__()
        self._from = from_
        self._to = to_
        self.step_size_in_days = step_size_in_days

    ################################ build() ################################
    def build(self) -> Tuple[str]:
        all_urls = []
        while self._to.is_after(self._from):
            url_str = self.format_url()
            all_urls.append(url_str)
            self._from = self._from.add_days(self.step_size_in_days)
        self.log_info(f"{self.__class__.__name__} built {len(all_urls)} urls")
        return tuple(all_urls)


# ------------------------------- AtmotubeTimeIterableURL ------------------------------- #
class AtmotubeTimeIterableURL(TimeIterableURLBuilderABC):

    def __init__(self, url: privateurl.PrivateURLBuilder, from_: tstype.Timestamp, to_: tstype.Timestamp, step_size_in_days: int = 1):
        super(AtmotubeTimeIterableURL, self).__init__(from_=from_, to_=to_, step_size_in_days=step_size_in_days)
        self._url = url.format_url() + "&date={date}"

    ################################ format_url() ################################
    def format_url(self) -> str:
        date = self._from.ts.split(' ')[0]
        return self._url.format(date=date)


# ------------------------------- ThingspeakTimeIterableURL ------------------------------- #
class ThingspeakTimeIterableURL(TimeIterableURLBuilderABC):

    def __init__(self, url: privateurl.PrivateURLBuilder, from_: tstype.Timestamp, to_: tstype.Timestamp, step_size_in_days: int = 7):
        super(ThingspeakTimeIterableURL, self).__init__(from_=from_, to_=to_, step_size_in_days=step_size_in_days)
        self._url = url.format_url() + "&start={start}&end={end}"

    ################################ format_url() ################################
    def format_url(self) -> str:
        start = self._from.ts.replace(" ", "%20")
        end = self._get_end_timestamp()
        return self._url.format(start=start, end=end)

    ################################ get_end_timestamp() ################################
    def _get_end_timestamp(self) -> str:
        tmp_end = self._from.add_days(self.step_size_in_days)
        if tmp_end.is_after(self._to):
            tmp_end = self._to
        return tmp_end.ts.replace(" ", "%20")
