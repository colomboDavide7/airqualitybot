######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:33
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Tuple
import airquality.api.url.abc as urlabc


# ------------------------------- PurpleairURLBuilder ------------------------------- #
class PurpleairURLBuilder(urlabc.URLBuilderABC):

    def __init__(self, url: str):
        self._url = url

    ################################ build() ################################
    def build(self) -> Tuple[str]:
        return tuple(self._url)
