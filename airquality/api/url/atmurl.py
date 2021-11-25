######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:32
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.api.url.baseurl as base


class AtmotubeURLBuilder(base.BaseURLBuilder):

    def __init__(self, address: str, key: str, mac: str):
        super(AtmotubeURLBuilder, self).__init__(address=address)
        self.url += f"?api_key={key}&mac={mac}"

    def build(self) -> str:
        return self.url

    def with_date(self, date: str):
        self.url += f"&date={date}"
        return self
