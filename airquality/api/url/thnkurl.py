######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:32
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.api.url.baseurl as base


class ThingspeakURLBuilder(base.BaseURLBuilder):

    def __init__(self, address: str, channel_id: str, key: str, format_: str):
        super(ThingspeakURLBuilder, self).__init__(address=address)
        self.url += f"/{channel_id}/feeds.{format_}?api_key={key}"

    def build(self) -> str:
        return self.url

    def with_start_timestamp(self, start: str):
        self.url += f"&start={start}"
        return self

    def with_end_timestamp(self, end: str):
        self.url += f"&end={end}"
        return self
