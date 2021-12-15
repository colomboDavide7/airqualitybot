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
import airquality.types.timest as tstype


class APIRepoABC(abc.ABC):

    def fetch(self, url: str) -> str:
        try:
            return urlopen(url).read()
        except (ValueError, URLError) as err:
            raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__class__} exception in {self.fetch.__name__} => {err!r}")


class NTimesAPIRepo(APIRepoABC):

    def __init__(self, url: str, ntimes=1):
        self.url = url
        self.ntimes = ntimes

    def __iter__(self):
        for _ in range(self.ntimes):
            yield super().fetch(url=self.url)


class TimeIterableAPIRepoABC(APIRepoABC, abc.ABC):

    def __init__(self, url: str, begin: tstype.TimestABC, stop: tstype.TimestABC, step_size_in_days=1):
        self.url = url
        self.begin = begin
        self.stop = stop
        self.step_size_in_days = step_size_in_days

    def __iter__(self):
        while self.stop.is_after(self.begin):
            yield super().fetch(url=self.format_url())
            self.begin = self.begin.add_days(days=self.step_size_in_days)

    @abc.abstractmethod
    def format_url(self) -> str:
        pass

    def _get_next_iteration_end_date(self) -> tstype.TimestABC:
        tmp_end = self.begin.add_days(days=self.step_size_in_days)
        if tmp_end.is_after(self.stop):
            return self.stop
        return tmp_end


class AtmotubeTimeIterableRepo(TimeIterableAPIRepoABC):

    def __init__(self, url: str, begin: tstype.TimestABC, stop: tstype.TimestABC, step_size_in_days=1):
        super(AtmotubeTimeIterableRepo, self).__init__(url=url, begin=begin, stop=stop, step_size_in_days=step_size_in_days)

    def format_url(self) -> str:
        date = self.begin.ts.split(' ')[0]
        return f"{self.url}&date={date}"


class ThingspeakTimeIterableAPIRepo(TimeIterableAPIRepoABC):

    def __init__(self, url: str, begin: tstype.TimestABC, stop: tstype.TimestABC, step_size_in_days=1):
        super(ThingspeakTimeIterableAPIRepo, self).__init__(url=url, begin=begin, stop=stop, step_size_in_days=step_size_in_days)

    def format_url(self) -> str:
        start = self.begin.ts.replace(" ", "%20")
        end = super()._get_next_iteration_end_date().ts.replace(" ", "%20")
        return f"{self.url}&start={start}&end={end}"
