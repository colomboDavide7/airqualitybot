######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:33
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.api.url.baseurl as base


class PurpleairURLBuilder(base.BaseURLBuilder):

    def __init__(self, address: str, key: str, fields: List[str]):
        super(PurpleairURLBuilder, self).__init__(address=address)
        fields_string = ','.join(f"{f}" for f in fields)
        self.url += f"?api_key={key}&fields={fields_string}"

    def build(self) -> str:
        return self.url

    def with_bounding_box(self, nwlat: float, nwlng: float, selat: float, selng: float):
        self.url += f"&nwlat={nwlat}&nwlng={nwlng}&selat={selat}&selng={selng}"
        return self
