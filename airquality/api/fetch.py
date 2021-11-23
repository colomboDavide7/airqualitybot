######################################################
#
# Author: Davide Colombo
# Date: 15/11/21 12:39
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict, Any
import airquality.api.util.url as bldr
import airquality.api.model as mdl
import airquality.file.util.parser as parse
import airquality.api.util.request as fetch
import airquality.logger.loggable as log
import airquality.logger.util.decorator as log_decorator


class FetchWrapper(log.Loggable):

    def __init__(
            self,
            url_builder: bldr.URLBuilder,
            response_builder: mdl.RESP_MODEL_BUILDER_TYPE,
            parser: parse.TextParser,
            log_filename="log"
    ):
        super(FetchWrapper, self).__init__(log_filename=log_filename)
        self.url_builder = url_builder
        self.response_builder = response_builder
        self.response_parser = parser
        self.channel_name = ""

    def update_url_param(self, param2update: Dict[str, Any]):
        self.url_builder.url_param.update(param2update)

    def set_channel_name(self, name: str):
        self.channel_name = name

    @log_decorator.log_decorator
    def get_sensor_data(self) -> List[mdl.RESP_MODEL_TYPE]:
        url = self.url_builder.url()
        response_text = fetch.fetch_from_url(url)
        parsed_response = self.response_parser.parse(response_text)
        responses = self.response_builder.get_responses(parsed_response=parsed_response)

        msg = f"{FetchWrapper.__name__}: fetched {len(responses)} sensor data"
        self.log_warning(msg) if len(responses) == 0 else self.log_info(msg)

        return responses
