######################################################
#
# Author: Davide Colombo
# Date: 24/12/21 18:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from abc import abstractmethod
from collections.abc import Iterable
from datetime import datetime, timedelta

DATE_FMT = "%Y-%m-%d"
SQL_DATETIME_FMT = "%Y-%m-%d %H:%M:%S"


class URLFormatter(object):

    def __init__(self, url_template: str, **options):
        self.url_template = url_template
        self.fmt_options = options

    def format_url(self, **options):
        options.update(self.fmt_options)
        return self.url_template.format(**options)

    def __repr__(self):
        return f"{type(self).__name__}(url_template={self.url_template}, fmt_options={self.fmt_options!r})"


class TimeURLFormatter(Iterable, URLFormatter):

    def __init__(self, url_template: str, begin: datetime, until=datetime.now(), step_in_days=1, **options):
        super(TimeURLFormatter, self).__init__(url_template=url_template, **options)
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

    def __repr__(self):
        return super(TimeURLFormatter, self).__repr__().strip(')') + \
               f", begin={self.begin}, until={self.until}, step_in_days={self.step_in_days})"


class AtmotubeTimeURLFormatter(TimeURLFormatter):
    DATE_KW = 'date'

    def __init__(self, url_template: str, begin: datetime, until=datetime.now(), step_in_days=1):
        super(AtmotubeTimeURLFormatter, self).__init__(url_template=url_template, begin=begin, until=until, step_in_days=step_in_days)
        self.url_template += "&date={%s}" % self.DATE_KW

    def next_args(self):
        tmp_end = self.begin
        tmp_end = self.until if tmp_end >= self.until else tmp_end

        return {self.DATE_KW: tmp_end.date().strftime(DATE_FMT)}


class ThingspeakTimeURLFormatter(TimeURLFormatter):
    START_KW = 'start'
    END_KW = 'end'

    def __init__(self, url_template: str, begin: datetime, until=datetime.now(), step_in_days=1):
        super(ThingspeakTimeURLFormatter, self).__init__(url_template=url_template, begin=begin, until=until, step_in_days=step_in_days)
        self.url_template += "&start={%s}&end={%s}" % (self.START_KW, self.END_KW)

    def next_args(self):
        tmp_end = self.begin + timedelta(days=self.step_in_days)
        tmp_end = self.until if tmp_end >= self.until else tmp_end

        start_ts = self.begin.strftime(SQL_DATETIME_FMT).replace(" ", "%20")
        end_ts = tmp_end.strftime(SQL_DATETIME_FMT).replace(" ", "%20")
        return {self.START_KW: start_ts, self.END_KW: end_ts}
