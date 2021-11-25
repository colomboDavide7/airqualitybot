######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:36
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Dict, Any


class BaseURLBuilder(abc.ABC):

    def __init__(self, address: str, options: Dict[str, Any]):
        self.address = address
        self.options = options

    @abc.abstractmethod
    def build(self) -> str:
        pass

    def with_options(self, options: Dict[str, Any]):
        self.options = options
        return self

    def _get_options_querystring(self) -> str:
        return '&'.join(f"{k}={v}" for k, v in self.options.items())
