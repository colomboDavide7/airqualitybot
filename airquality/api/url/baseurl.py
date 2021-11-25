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

    def __init__(self, address: str):
        self.url = address

    @abc.abstractmethod
    def build(self) -> str:
        pass

    def with_options(self, options: Dict[str, Any]):
        for key, val in options.items():
            self.url += f"&{key}={val}"
        return self
