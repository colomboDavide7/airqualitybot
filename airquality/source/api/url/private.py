######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 18:46
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.source.api.url.abc as urlabc


# ------------------------------- PrivateURLBuilderABC ------------------------------- #
class PrivateURLBuilderABC(urlabc.URLBuilderABC, abc.ABC):

    def __init__(self, url_template: str, api_key: str, ident: str, fmt: str):
        super(PrivateURLBuilderABC, self).__init__(url_template=url_template)
        self._api_key = api_key
        self._ident = ident
        self._fmt = fmt

    @property
    def ident(self):
        return self._ident

    @property
    def api_key(self):
        return self._api_key

    @property
    def fmt(self):
        return self._fmt


# ------------------------------- AtmotubeURLBuilder ------------------------------- #
class AtmotubeURLBuilder(PrivateURLBuilderABC):

    def __init__(self, url_template: str, api_key: str, ident: str, fmt: str):
        super(AtmotubeURLBuilder, self).__init__(url_template=url_template, api_key=api_key, ident=ident, fmt=fmt)

    ################################ build() ################################
    def build(self) -> str:
        return self.url_template.format(api_key=self._api_key, mac=self._ident, fmt=self._fmt)


# ------------------------------- ThingspeakURLBuilder ------------------------------- #
class ThingspeakURLBuilder(PrivateURLBuilderABC):

    def __init__(self, url_template: str, api_key: str, ident: str, fmt: str):
        super(ThingspeakURLBuilder, self).__init__(url_template=url_template, api_key=api_key, ident=ident, fmt=fmt)

    ################################ build() ################################
    def build(self) -> str:
        return self.url_template.format(channel_id=self._ident, api_key=self._api_key, fmt=self._fmt)
