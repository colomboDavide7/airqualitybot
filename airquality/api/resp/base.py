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
