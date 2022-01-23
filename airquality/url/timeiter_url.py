######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 14:33
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.core.iteritems import IterableItemsABC
from airquality.extra.timest import make_naive
from datetime import datetime, timedelta
from abc import abstractmethod
from typing import Generator

ISO_DATETIME_FMT = "%Y-%m-%d %H:%M:%S"              # e.g., 2021-10-11 09:44:37


def _get_smallest_between(time: datetime, upper_bound: datetime):
    """
    A function that compare the *time* to the *upper_bound* and return the smallest.
    """

    return upper_bound if time >= upper_bound else time


class TimeIterableURL(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the basic business rules for building and formatting a URL by adding time
    optional parameters.
    """

    def __init__(
        self,
        url: str,                           # the url to decorate with time range.
        begin: datetime,                    # the datetime object that defines the starting point for generating urls.
        until=datetime.now(),               # the datetime object that defines the upper bound for generating urls.
        step_size_in_days=1                 # the time loop's step size in days.
    ):
        self.url = url
        self.begin = make_naive(begin)
        self.until = make_naive(until)
        self.step_size_in_days = step_size_in_days

    def add_days_to(self, timestamp: datetime):
        return timestamp + timedelta(days=self.step_size_in_days)

    @abstractmethod
    def format_time(self, time: datetime):
        """A method that a subclass must override to explicitly define how to format a datetime object."""
        pass

    @abstractmethod
    def format_url(self, begin: datetime, until: datetime) -> str:
        """A method that a subclass must override to explicitly define how to format the url string."""
        pass

    def items(self) -> Generator[str, None, None]:
        tmp_begin = self.begin
        tmp_until = self.until
        while tmp_begin <= tmp_until:
            yield self.format_url(begin=tmp_begin, until=tmp_until)
            tmp_begin = self.add_days_to(tmp_begin)

    def __repr__(self):
        return f"{type(self).__name__}(url='{self.url}', begin='{self.begin}', until='{self.until}', " \
               f"step_size_in_days='{self.step_size_in_days}')"


class AtmotubeTimeIterableURL(TimeIterableURL):
    """
    A *TimeIterableURL* that implements the *format_url* method and defines the details of formatting an Atmotube URL.
    """

    def format_url(self, begin: datetime, until: datetime) -> str:
        tmp_date = _get_smallest_between(time=begin, upper_bound=until)
        return f"{self.url}&date={self.format_time(tmp_date)}"

    def format_time(self, time: datetime):
        return time.date().strftime('%Y-%m-%d')


class ThingspeakTimeIterableURL(TimeIterableURL):
    """
    A *TimeIterableURL* that implements the *format_url* method and defines the details of formatting a Thingspeak URL.
    """

    def format_url(self, begin: datetime, until: datetime) -> str:
        tmp_until = _get_smallest_between(time=self.add_days_to(begin), upper_bound=until)
        return f"{self.url}&start={self.format_time(begin)}&end={self.format_time(tmp_until)}"

    def format_time(self, time: datetime):
        return time.strftime(ISO_DATETIME_FMT).replace(" ", "%20")
