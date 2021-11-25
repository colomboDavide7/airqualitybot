######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:32
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
import airquality.api.url.dynurl as dyn


class ThingspeakURLBuilder(dyn.DynamicURL):

    def __init__(self, address: str, options: Dict[str, Any], fmt: str):
        super(ThingspeakURLBuilder, self).__init__(address=address, options=options)
        self.format = fmt

    def build(self) -> str:
        return f"{self.address}/{self.identifier}/feeds.{self.format}?api_key={self.api_key}&{self._get_options_querystring()}"
