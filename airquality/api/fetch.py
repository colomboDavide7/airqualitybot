######################################################
#
# Author: Davide Colombo
# Date: 15/11/21 12:39
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict, Any
import airquality.api.util.url as bldr
import airquality.api.util.extractor as ext
import airquality.file.util.parser as parser
import airquality.api.util.request as fetch
import airquality.logger.loggable as log


class FetchWrapper(log.Loggable):

    def __init__(self, url_builder: bldr.URLBuilder, data_extractor: ext.DataExtractor, response_parser: parser.TextParser):
        super(FetchWrapper, self).__init__()
        self.builder = url_builder
        self.data_extractor = data_extractor
        self.response_parser = response_parser
        self.channel_name = ""

    def update_param(self, param2update: Dict[str, Any]):
        self.builder.url_param.update(param2update)

    def set_channel_name(self, channel_name: str):
        self.channel_name = channel_name

    def get_sensor_data(self) -> List[Dict[str, Any]]:

        url = self.builder.url()
        response_text = fetch.fetch_from_url(url)
        parsed_response = self.response_parser.parse(response_text)
        sensor_data = self.data_extractor.extract(parsed_response=parsed_response, channel_name=self.channel_name)

        # Log message
        self.info_messages.append(f"success => fetched {len(sensor_data)} measurements")
        self.log_messages()

        return sensor_data
