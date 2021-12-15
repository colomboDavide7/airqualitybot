######################################################
#
# Author: Davide Colombo
# Date: 15/12/21 11:57
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.types.timest as tstype


class URLFormatter(abc.ABC):

    def __init__(self, url: str):
        self.url = url

    @abc.abstractmethod
    def format(self, **options) -> str:
        pass


class AtmotubeURLFormatter(URLFormatter):

    def format(self, gofrom: tstype.TimestABC, until: tstype.TimestABC) -> str:
        date = gofrom.ts.split(' ')[0]
        return f"{self.url}&date={date}"


class ThingspeakFormatter(URLFormatter):

    def format(self, gofrom: tstype.TimestABC, until: tstype.TimestABC) -> str:
        start = gofrom.ts.replace(' ', '%20')
        end = until.ts.replace(' ', '%20')
        return f"{self.url}&start={start}&end={end}"
