######################################################
#
# Author: Davide Colombo
# Date: 22/12/21 17:06
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Iterable
from abc import abstractmethod
from datetime import datetime, timedelta

DATE_FMT = "%Y-%m-%d"
SQL_DATETIME_FMT = "%Y-%m-%d %H:%M:%S"


class IterableURL(Iterable):

    def __init__(self, url: str, begin: datetime, until=datetime.now(), step_in_days=1):
        self.url = url
        self.begin = begin
        self.until = until
        self.step_in_days = step_in_days

    @abstractmethod
    def next_date(self):
        pass

    def __iter__(self):
        while self.begin <= self.until:
            yield self.url.format(**self.next_date())
            self.begin += timedelta(days=self.step_in_days)

    def __len__(self):
        return ((self.until - self.begin).days // self.step_in_days) + 1

    def __repr__(self):
        return f"{type(self).__name__}(begin={self.begin}, until={self.until}, step_in_days={self.step_in_days}, url={self.url})"


class AtmotubeIterableURL(IterableURL):
    DATE_KW = 'date'

    def __init__(self, url: str, begin: datetime, until=datetime.now(), step_in_days=1):
        super(AtmotubeIterableURL, self).__init__(url=url, begin=begin, until=until, step_in_days=step_in_days)
        self.url += "&date={%s}" % self.DATE_KW

    def next_date(self):
        tmp_end = self.until if self.begin >= self.until else self.begin
        return {self.DATE_KW: tmp_end.date().strftime(DATE_FMT)}


class ThingspeakIterableURL(IterableURL):
    START_KW = 'start'
    END_KW = 'end'

    def __init__(self, url: str, begin: datetime, until=datetime.now(), step_in_days=7):
        super(ThingspeakIterableURL, self).__init__(url=url, begin=begin, until=until, step_in_days=step_in_days)
        self.url += "&start={%s}&end={%s}" % (self.START_KW, self.END_KW)

    def next_date(self):
        tmp_end = self.begin + timedelta(days=self.step_in_days)
        tmp_end = self.until if tmp_end >= self.until else tmp_end

        start_ts = self.begin.strftime(SQL_DATETIME_FMT).replace(" ", "%20")
        end_ts = tmp_end.strftime(SQL_DATETIME_FMT).replace(" ", "%20")
        return {self.START_KW: start_ts, self.END_KW: end_ts}
