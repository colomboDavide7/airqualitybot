######################################################
#
# Author: Davide Colombo
# Date: 09/12/21 18:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Generator
import airquality.source.api.abc as apisrcabc
import airquality.source.api.req.api_req as apireq
import airquality.source.api.url.private as privateurl
import airquality.source.api.resp.atmotube as resptype
import airquality.file.util.text_parser as textparser


# ------------------------------- AtmotubeAPISource ------------------------------- #
class AtmotubeAPISource(apisrcabc.APISourceABC):

    def __init__(self, url: privateurl.PrivateURL, parser: textparser.TextParser, builder: resptype.AtmotubeAPIRespBuilder):
        self.url = url
        self.parser = parser
        self.builder = builder

    ################################ get() ################################
    def get(self) -> Generator[List[resptype.AtmotubeAPIRespType], None, None]:
        url_generator = self.url.build()
        for url2fetch in url_generator:
            raw_responses = apireq.fetch_from_url(url2fetch)
            parsed_responses = self.parser.parse(raw_responses)
            yield self.builder.build(parsed_responses)
