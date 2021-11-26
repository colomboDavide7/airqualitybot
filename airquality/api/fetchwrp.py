######################################################
#
# Author: Davide Colombo
# Date: 15/11/21 12:39
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Union
import airquality.logger.loggable as log
import airquality.logger.util.decorator as log_decorator
import airquality.api.request as apireq
import airquality.api.resp.base as apibuild
import airquality.file.util.parser as parse
import airquality.types.apiresp.measresp as measresp
import airquality.types.apiresp.inforesp as inforesp

RETURNED_TYPE = Union[measresp.MeasureAPIResp, inforesp.SensorInfoResponse]


class FetchWrapper(log.Loggable):

    def __init__(self, resp_builder: apibuild.APIRespBuilder, resp_parser: parse.TextParser, log_filename="log"):
        super(FetchWrapper, self).__init__(log_filename=log_filename)
        self.resp_builder = resp_builder
        self.resp_parser = resp_parser

    @log_decorator.log_decorator
    def fetch(self, url: str) -> List[RETURNED_TYPE]:
        raw_resp = apireq.fetch_from_url(url)
        parsed_resp = self.resp_parser.parse(raw_resp)
        api_responses = self.resp_builder.build(parsed_resp)

        msg = f"{FetchWrapper.__name__}: fetched {len(api_responses)} sensor data"
        self.log_warning(msg) if len(api_responses) == 0 else self.log_info(msg)

        return api_responses
