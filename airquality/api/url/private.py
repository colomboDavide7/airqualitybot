######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 18:46
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Tuple
import airquality.api.url.abc as urlabc


# ------------------------------- PrivateURLBuilderABC ------------------------------- #
class PrivateURLBuilder(urlabc.URLBuilderABC):

    def __init__(self, url: str, key: str, ident: str, fmt: str):
        self._url = url
        self._key = key
        self._ident = ident
        self._fmt = fmt

    def build(self) -> Tuple[str]:
        return tuple(self.format_url())

    def format_url(self) -> str:
        return self._url.format(key=self._key, ident=self._ident, fmt=self._fmt)
