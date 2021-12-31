######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 14:33
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.core.iteritems import IterableItemsABC
from datetime import datetime, timedelta
from typing import Generator


class AtmotubeTimeIterableURL(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules for properly format an Atmotube URL by adding
    the *date* parameter in the querystring.
    The output is a Generator of formatted urls starting from *begin* to *until*.
    """

    def __init__(self, url: str, begin: datetime, until=datetime.now(), step_size_in_days=1):
        self.url = url + "&date={date}"
        self.begin = begin
        self.until = until
        self.step_size_in_days = step_size_in_days

    def items(self) -> Generator[str, None, None]:
        tmp_begin = self.begin
        tmp_until = self.until
        while tmp_begin <= tmp_until:
            tmp_date = tmp_until if tmp_begin >= tmp_until else tmp_begin
            yield self.url.format(date=tmp_date.date().strftime("%Y-%m-%d"))
            tmp_begin += timedelta(days=self.step_size_in_days)
