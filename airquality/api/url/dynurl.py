######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 18:46
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Dict, Any
import airquality.api.url.baseurl as base


class DynamicURL(base.BaseURLBuilder, abc.ABC):

    def __init__(self, address: str, options: Dict[str, Any]):
        super(DynamicURL, self).__init__(address=address, options=options)
        self.api_key = None
        self.identifier = None

    def with_api_key(self, api_key: str):
        self.api_key = api_key
        return self

    def with_identifier(self, ident: str):
        self.identifier = ident
        return self
