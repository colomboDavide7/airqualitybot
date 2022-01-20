######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 14:33
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.core.iteritems import IterableItemsABC
from airquality.datamodel.timest import Timest
from datetime import datetime, timedelta
from typing import Generator
from abc import abstractmethod


class TimeIterableURL(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the basic business rules for building and formatting a URL by adding time
    optional parameters.
    """
    TIMESTAMP_FMT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, url: str, begin: datetime, until=Timest.current_utc_timetz(), step_size_in_days=1):
        self.url = url
        self.begin = begin
        self.until = until
        self.step_size_in_days = step_size_in_days

    def add_days_to(self, timestamp: datetime):
        return timestamp + timedelta(days=self.step_size_in_days)

    def datetime_to_string(self, timestamp: datetime):
        return timestamp.strftime(self.TIMESTAMP_FMT).replace(" ", "%20")

    def get_tmp_timest(self, tmp_end: datetime, until: datetime):
        return until if tmp_end >= until else tmp_end

    @abstractmethod
    def format_url(self, begin: datetime, until: datetime) -> str:
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
        timest = self.get_tmp_timest(tmp_end=begin, until=until)
        return f"{self.url}&date={timest.date().strftime('%Y-%m-%d')}"


class ThingspeakTimeIterableURL(TimeIterableURL):
    """
    A *TimeIterableURL* that implements the *format_url* method and defines the details of formatting a Thingspeak URL.
    """

    def format_url(self, begin: datetime, until: datetime) -> str:
        tmp_timest = self.get_tmp_timest(tmp_end=self.add_days_to(begin), until=until)
        return f"{self.url}&start={self.datetime_to_string(begin)}&end={self.datetime_to_string(tmp_timest)}"
