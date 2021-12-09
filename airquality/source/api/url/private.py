######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 18:46
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import source.api.url.baseurl as base


class PrivateURL(base.BaseURLBuilder, abc.ABC):

    def __init__(self, url_template: str):
        super(PrivateURL, self).__init__(url_template=url_template)
        self.api_key = None
        self.ident = None

    def with_api_key(self, api_key: str):
        self.api_key = api_key
        return self

    def with_identifier(self, ident: str):
        self.ident = ident
        return self


############################# ATMOTUBE URL BUILDER ##############################
class AtmotubeURLBuilder(PrivateURL):

    def __init__(self, url_template: str):
        super(AtmotubeURLBuilder, self).__init__(url_template=url_template)

    def build(self) -> str:
        return self.url_template.format(api_key=self.api_key, mac=self.ident, fmt=self.fmt)


############################# THINGSPEAK URL BUILDER ##############################
class ThingspeakURLBuilder(PrivateURL):

    def __init__(self, url_template: str):
        super(ThingspeakURLBuilder, self).__init__(url_template=url_template)

    def build(self) -> str:
        return self.url_template.format(channel_id=self.ident, api_key=self.api_key, fmt=self.fmt)
