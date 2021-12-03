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
import airquality.file.util.text_parser as parse


class FetchWrapper(log.Loggable):

    def __init__(self, resp_parser: parse.FileParser, log_filename="log"):
        super(FetchWrapper, self).__init__(log_filename=log_filename)
        self.resp_parser = resp_parser

    @log_decorator.log_decorator
    def fetch(self, url: str) -> Dict[str, Any]:
        return self.resp_parser.parse(apireq.fetch_from_url(url))
