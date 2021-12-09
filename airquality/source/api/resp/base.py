######################################################
#
# Author: Davide Colombo
# Date: 26/11/21 08:51
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Dict, Any


class APIRespBuilder(abc.ABC):

    @abc.abstractmethod
    def build(self, parsed_resp: Dict[str, Any]):
        pass

    @abc.abstractmethod
    def exit_on_bad_item(self, item: Dict[str, Any]) -> None:
        pass

    @abc.abstractmethod
    def exit_on_bad_parsed_response(self, parsed_resp: Dict[str, Any]) -> None:
        pass
