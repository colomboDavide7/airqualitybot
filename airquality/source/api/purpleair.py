######################################################
#
# Author: Davide Colombo
# Date: 09/12/21 18:32
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.source.api.abc as apisrcabc
import airquality.source.api.url.purpleair as purpurl
import airquality.source.api.resp.purpleair as resptype
import airquality.file.util.text_parser as textparser
import airquality.source.api.api_req as apirequest


# ------------------------------- PurpleairAPISource ------------------------------- #
class PurpleairAPISource(apisrcabc.APISourceABC):

    def __init__(
            self,
            url: purpurl.PurpleairURLBuilder,
            parser: textparser.TextParser,
            builder: resptype.PurpleairAPIRespBuilder,
            request: apirequest.APIRequest,
            log_filename="log"
    ):
        super(PurpleairAPISource, self).__init__(api_request=request, log_filename=log_filename)
        self.url = url
        self.parser = parser
        self.builder = builder

    ################################ get() ################################
    def get(self) -> List[resptype.PurpleairAPIRespType]:
        url2fetch = self.url.build()
        raw_response = self.api_request.fetch_from_url(url2fetch)
        parsed_response = self.parser.parse(raw_response)
        return self.builder.build(parsed_response)
