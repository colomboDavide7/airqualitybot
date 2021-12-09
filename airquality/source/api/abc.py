######################################################
#
# Author: Davide Colombo
# Date: 08/12/21 19:11
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List
import airquality.source.abc as basesource


# ------------------------------- APIResponseType ------------------------------- #
class APIResponseType(abc.ABC):
    pass


# ------------------------------- APISourceABC ------------------------------- #
class APISourceABC(basesource.SourceABC, abc.ABC):

    @abc.abstractmethod
    def get(self) -> List[APIResponseType]:
        pass
