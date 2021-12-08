######################################################
#
# Author: Davide Colombo
# Date: 08/12/21 19:11
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Generator
import airquality.source.source as basesource
import airquality.file.util.text_parser as textparser
import airquality.api.request as apireq


class APISourceABC(basesource.SourceABC, abc.ABC):
    pass


import airquality.api.url.public as purpurl
import airquality.api.resp.info.purpleair as purpbuilder
import airquality.types.apiresp.inforesp as infotype


class PurpleairAPISource(APISourceABC):

    def __init__(self, url: purpurl.PurpleairURLBuilder, parser: textparser.TextParser, builder: purpbuilder.PurpleairAPIRespBuilder):
        self.url = url
        self.parser = parser
        self.builder = builder

    def get(self) -> Generator[infotype.SensorInfoResponse, None, None]:
        url2fetch = self.url.build()
        raw_response = apireq.fetch_from_url(url2fetch)
        parsed_response = self.parser.parse(raw_response)
        return self.builder.build(parsed_response)
