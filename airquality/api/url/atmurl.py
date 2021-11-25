######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:32
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
import airquality.api.url.dynurl as dyn


class AtmotubeURLBuilder(dyn.DynamicURL):

    def __init__(self, address: str, options: Dict[str, Any]):
        super(AtmotubeURLBuilder, self).__init__(address=address, options=options)
        self.date = None

    def build(self) -> str:
        return f"{self.address}?api_key={self.api_key}&mac={self.identifier}&{self._get_options_querystring()}"
