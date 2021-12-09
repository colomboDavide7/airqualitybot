######################################################
#
# Author: Davide Colombo
# Date: 08/12/21 19:11
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Generator, List
import airquality.source.source as basesource
import airquality.file.util.text_parser as textparser
import airquality.api.request as apireq


class APISourceABC(basesource.SourceABC, abc.ABC):
    pass


################################ PURPLEAIR API SOURCE ###############################
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


################################ ATMOTUBE API SOURCE ###############################
import airquality.api.url.private as privateurl
import airquality.api.resp.measure.atmotube as atmbuilder
import airquality.types.apiresp.measresp as measuretype


class AtmotubeAPISource(APISourceABC):

    def __init__(self, url: privateurl.PrivateURL, parser: textparser.TextParser, builder: atmbuilder.AtmotubeAPIRespBuilder):
        self.url = url
        self.parser = parser
        self.builder = builder

    def get(self) -> Generator[List[measuretype.MobileSensorAPIResp], None, None]:
        url_generator = self.url.build()
        for url2fetch in url_generator:
            raw_responses = apireq.fetch_from_url(url2fetch)
            parsed_responses = self.parser.parse(raw_responses)
            yield self.builder.build(parsed_responses)
