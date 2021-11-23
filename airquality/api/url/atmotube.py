######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:32
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
import airquality.api.url.base as base


################################ ATMOTUBE URL BUILDER ################################
class AtmotubeURL(base.BaseURL):

    def __init__(self, address: str, parameters: Dict[str, Any]):
        super(AtmotubeURL, self).__init__(address=address, parameters=parameters)

    def url(self) -> str:
        self._exit_on_bad_url_parameters()
        return f"{self.address}?{self._get_querystring()}"

    def _exit_on_bad_url_parameters(self):
        if 'api_key' not in self.parameters:
            raise SystemExit(f"{AtmotubeURL.__name__}: bad url param => missing key='api_key'")
        elif 'mac' not in self.parameters:
            raise SystemExit(f"{AtmotubeURL.__name__}: bad url param => missing key='mac'")
