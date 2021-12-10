######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 18:46
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Tuple
import airquality.api.url.abc as urlabc


# ------------------------------- PrivateURLBuilderABC ------------------------------- #
class PrivateURLBuilderABC(urlabc.URLBuilderABC, abc.ABC):

    def __init__(self, url: str, api_key: str, ident: str, fmt: str):
        self._url = url
        self._api_key = api_key
        self._ident = ident
        self._fmt = fmt

    @property
    def ident(self) -> str:
        return self._ident

    @property
    def api_key(self) -> str:
        return self._api_key

    @property
    def fmt(self) -> str:
        return self._fmt

    @property
    def url(self) -> str:
        return self._url


# ------------------------------- AtmotubeURLBuilder ------------------------------- #
class AtmotubeURLBuilder(PrivateURLBuilderABC):

    def __init__(self, url: str, api_key: str, ident: str, fmt: str):
        super(AtmotubeURLBuilder, self).__init__(url=url, api_key=api_key, ident=ident, fmt=fmt)

    ################################ build() ################################
    def build(self) -> Tuple[str]:
        return tuple(self._url.format(api_key=self._api_key, mac=self._ident, fmt=self._fmt))


# ------------------------------- ThingspeakURLBuilder ------------------------------- #
class ThingspeakURLBuilder(PrivateURLBuilderABC):

    def __init__(self, url: str, api_key: str, ident: str, fmt: str):
        super(ThingspeakURLBuilder, self).__init__(url=url, api_key=api_key, ident=ident, fmt=fmt)

    ################################ build() ################################
    def build(self) -> Tuple[str]:
        return tuple(self._url.format(channel_id=self._ident, api_key=self._api_key, fmt=self._fmt))
