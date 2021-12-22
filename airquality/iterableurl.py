######################################################
#
# Author: Davide Colombo
# Date: 22/12/21 17:06
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Iterable
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

DATE_FMT = "%Y-%m-%d"
SQL_DATETIME_FMT = "%Y-%m-%d %H:%M:%S"


class IterableURL(Iterable, ABC):

    def __init__(self, url_template: str, begin: datetime, until: datetime, step_in_days=1):
        self.url_template = url_template
        self.begin = begin
        self.until = until
        self.step_in_days = step_in_days

    @abstractmethod
    def next_args(self):
        pass

    def __iter__(self):
        while self.begin <= self.until:
            yield self.url_template.format(**self.next_args())
            self.begin += timedelta(days=self.step_in_days)

    def __len__(self):
        return ((self.until - self.begin).days // self.step_in_days) + 1


class AtmotubeIterableURL(IterableURL):
    DATE_KW = 'date'

    def __init__(self, url_template: str, begin: datetime, until: datetime, step_in_days=1):
        super(AtmotubeIterableURL, self).__init__(url_template=url_template, begin=begin, until=until, step_in_days=step_in_days)
        self.url_template += "&date={%s}" % self.DATE_KW

    def next_args(self):
        tmp_end = self.begin
        tmp_end = self.until if tmp_end >= self.until else tmp_end

        return {self.DATE_KW: tmp_end.date().strftime(DATE_FMT)}


class ThingspeakIterableURL(IterableURL):
    START_KW = 'start'
    END_KW = 'end'

    def __init__(self, url_template: str, begin: datetime, until: datetime, step_in_days=1):
        super(ThingspeakIterableURL, self).__init__(url_template=url_template, begin=begin, until=until, step_in_days=step_in_days)
        self.url_template += "&start={%s}&end={%s}" % (self.START_KW, self.END_KW)

    def next_args(self):
        tmp_end = self.begin + timedelta(days=self.step_in_days)
        tmp_end = self.until if tmp_end >= self.until else tmp_end

        start_ts = self.begin.strftime(SQL_DATETIME_FMT).replace(" ", "%20")
        end_ts = tmp_end.strftime(SQL_DATETIME_FMT).replace(" ", "%20")
        return {self.START_KW: start_ts, self.END_KW: end_ts}
