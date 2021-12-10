######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:33
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Tuple
import airquality.api.url.abc as base


# ------------------------------- PurpleairURLBuilder ------------------------------- #
class PurpleairURLBuilder(base.URLBuilderABC):

    def __init__(self, url: str):
        self.url = url

    ################################ build() ################################
    def build(self) -> Tuple[str]:
        return tuple(self.url)
