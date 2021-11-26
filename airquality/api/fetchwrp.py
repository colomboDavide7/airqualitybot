######################################################
#
# Author: Davide Colombo
# Date: 15/11/21 12:39
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
import airquality.logger.loggable as log
import airquality.logger.util.decorator as log_decorator
import airquality.api.request as apireq
import airquality.file.util.parser as parse


class FetchWrapper(log.Loggable):

    def __init__(self, resp_parser: parse.TextParser, log_filename="log"):
        super(FetchWrapper, self).__init__(log_filename=log_filename)
        self.resp_parser = resp_parser

    @log_decorator.log_decorator
    def fetch(self, url: str) -> Dict[str, Any]:
        # msg = f"{FetchWrapper.__name__}: fetched {len(api_responses)} sensor data"
        # self.log_warning(msg) if len(api_responses) == 0 else self.log_info(msg)

        return self.resp_parser.parse(
            text=apireq.fetch_from_url(
                url=url
            )
        )
