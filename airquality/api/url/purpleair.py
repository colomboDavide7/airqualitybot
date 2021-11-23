######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:33
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
import airquality.api.url.base as base


class PurpleairURL(base.BaseURL):

    def __init__(self, address: str, parameters: Dict[str, Any]):
        super(PurpleairURL, self).__init__(address=address, parameters=parameters)

    def url(self) -> str:
        self._exit_on_bad_url_parameters()
        return f"{self.address}?{self._get_fields_string()}&{self._get_querystring()}"

    def _get_fields_string(self) -> str:
        return "fields=" + ','.join(f"{f}" for f in self.parameters.pop('fields'))

    def _exit_on_bad_url_parameters(self):
        if 'api_key' not in self.parameters:
            raise SystemExit(f"{PurpleairURL.__name__}: bad url param => missing key='api_key'")
        elif 'fields' not in self.parameters:
            raise SystemExit(f"{PurpleairURL.__name__}: bad url param => missing key='fields'")
        elif not self.parameters['fields']:
            raise SystemExit(f"{PurpleairURL.__name__}: bad url param => empty fields.")