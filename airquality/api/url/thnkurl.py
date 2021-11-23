######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:32
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
import airquality.api.url.baseurl as base


################################ THINGSPEAK URL BUILDER ################################
class ThingspeakURL(base.BaseURL):

    def __init__(self, address: str, url_param: Dict[str, Any]):
        super(ThingspeakURL, self).__init__(address=address, parameters=url_param)

        if 'format' not in self.parameters:
            raise SystemExit(f"{ThingspeakURL.__name__}: bad 'api.json' file structure => missing key='format'")
        self.response_fmt = self.parameters.pop('format')

    def url(self) -> str:
        self._exit_on_bad_url_parameters()
        url = f"{self.address}/{self.parameters['channel_id']}/feeds.{self.response_fmt}?{self._get_querystring()}"
        return url.replace(' ', '%20')

    def _get_querystring(self):
        return '&'.join(f"{n}={v}" for n, v in self.parameters.items() if n != 'channel_id')

    def _exit_on_bad_url_parameters(self):
        if 'api_key' not in self.parameters:
            raise SystemExit(f"{ThingspeakURL.__name__}: bad url param => missing key='api_key'")
        elif 'channel_id' not in self.parameters:
            raise SystemExit(f"{ThingspeakURL.__name__}: bad url param => missing key='channel_id'")
