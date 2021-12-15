######################################################
#
# Author: Davide Colombo
# Date: 15/12/21 15:01
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from urllib.request import urlopen
from urllib.error import URLError
import airquality.api.urlfmt as urlfmt
import airquality.types.timest as tstype


class APIRepoABC(abc.ABC):

    def fetch(self, url: str) -> str:
        try:
            return urlopen(url).read()
        except (ValueError, URLError) as err:
            raise SystemExit(f"{self.__class__.__name__} catches "
                             f"{err.__class__.__name__} exception in"
                             f"{self.fetch.__name__} method => {err!r}")


class NTimesAPIRepo(APIRepoABC):

    def __init__(self, url: str, ntimes=1):
        self.url = url
        self.ntimes = ntimes

    def __iter__(self):
        for _ in range(self.ntimes):
            yield super().fetch(url=self.url)


class TimeIterableAPIRepo(APIRepoABC):

    def __init__(
            self,
            formatter: urlfmt.URLFormatter,
            begin: tstype.TimestABC, stop: tstype.TimestABC,
            step_in_days=1
    ):
        self.formatter = formatter
        self.begin = begin
        self.stop = stop
        self.step_in_days = step_in_days

    @property
    def until(self) -> tstype.TimestABC:
        until = self.begin.add_days(days=self.step_in_days)
        if until.is_after(self.stop):
            until = self.stop
        return until

    def __iter__(self):
        while self.stop.is_after(self.begin):
            url = self.formatter.format(gofrom=self.begin, until=self.until)
            yield super().fetch(url)
            self.begin = self.begin.add_days(days=self.step_in_days)
