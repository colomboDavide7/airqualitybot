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
import airquality.file.util.parser as parse
import airquality.api.util.request as fetch
import airquality.logger.loggable as log


class FetchWrapper(log.Loggable):

    def __init__(self, url_builder: bldr.URLBuilder, extractor: ext.DataExtractor, parser: parse.TextParser):
        super(FetchWrapper, self).__init__()
        self.builder = url_builder
        self.data_extractor = extractor
        self.response_parser = parser
        self.channel_name = ""

    def update_url_param(self, param2update: Dict[str, Any]):
        self.builder.url_param.update(param2update)

    def set_channel_name(self, name: str):
        self.channel_name = name

    def get_sensor_data(self) -> List[Dict[str, Any]]:

        self.log_info(f"{FetchWrapper.__name__}: try to fetch sensor data...")
        url = self.builder.url()
        response_text = fetch.fetch_from_url(url)
        parsed_response = self.response_parser.parse(response_text)
        sensor_data = self.data_extractor.extract(parsed_response=parsed_response, channel_name=self.channel_name)

        msg = f"...fetched {len(sensor_data)} sensor data..."
        self.log_warning(msg) if len(sensor_data) == 0 else self.log_info(msg)
        self.log_info(f"{FetchWrapper.__name__}: done")

        return sensor_data
