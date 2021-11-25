######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:33
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict, Any
import airquality.api.url.baseurl as base


class PurpleairURLBuilder(base.BaseURLBuilder):

    def __init__(self, address: str, options: Dict[str, Any], key: str, fields: List[str], bounding_box: Dict[str, Any]):
        super(PurpleairURLBuilder, self).__init__(address=address, options=options)
        self.fields = fields
        self.key = key
        self.bounding_box = bounding_box

    def build(self) -> str:
        return f"{self.address}?api_key={self.key}&{self._get_fields_querystring()}" \
               f"&{self._get_bounding_box_querystring()}&{self._get_options_querystring()}"

    def _get_fields_querystring(self) -> str:
        return "fields=" + ','.join(f"{f}" for f in self.fields)

    def _get_bounding_box_querystring(self) -> str:
        return '&'.join(f"{key}={val}" for key, val in self.bounding_box.items())
