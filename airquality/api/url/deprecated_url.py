######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 20:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import api.urlfmt as urlabc
import airquality.types.timest as tstype


# ------------------------------- TimeIterableURLBuilderABC ------------------------------- #
class TimeIterableURLFormatterABC(urlabc.URLFormatter, abc.ABC):

    def __init__(self, url: str, from_: tstype.TimestABC, to_: tstype.TimestABC, step_size_in_days: int = 1):
        super(TimeIterableURLFormatterABC, self).__init__()
        self._url = url
        self._from = from_
        self._to = to_
        self.step_size_in_days = step_size_in_days

    def __iter__(self):
        while self._to.is_after(self._from):
            yield self.format_url()
            self._from = self._from.add_days(self.step_size_in_days)


# ------------------------------- AtmotubeTimeFormatter ------------------------------- #
class AtmotubeTimeIterableURLFormatter(TimeIterableURLFormatterABC):

    def __init__(self, url: str, from_: tstype.TimestABC, to_: tstype.TimestABC, step_size_in_days: int = 1):
        super(AtmotubeTimeIterableURLFormatter, self).__init__(url=url, from_=from_, to_=to_, step_size_in_days=step_size_in_days)

    ################################ format_url() ################################
    def format_url(self) -> str:
        date = self._from.ts.split(' ')[0]
        return f"{self._url}&date={date}"


# ------------------------------- ThingspeakTimeFormatter ------------------------------- #
class ThingspeakTimeIterableURLFormatter(TimeIterableURLFormatterABC):

    def __init__(self, url: str, from_: tstype.TimestABC, to_: tstype.TimestABC, step_size_in_days: int = 7):
        super(ThingspeakTimeIterableURLFormatter, self).__init__(url=url, from_=from_, to_=to_, step_size_in_days=step_size_in_days)

    ################################ format_url() ################################
    def format_url(self) -> str:
        start = self._from.ts.replace(" ", "%20")
        end = self._get_end_timestamp()
        return f"{self._url}&start={start}&end={end}"

    ################################ _get_end_timestamp() ################################
    def _get_end_timestamp(self) -> str:
        tmp_end = self._from.add_days(self.step_size_in_days)
        if tmp_end.is_after(self._to):
            tmp_end = self._to
        return tmp_end.ts.replace(" ", "%20")
