######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:36
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Tuple


# ------------------------------- URLBuilderABC ------------------------------- #
class URLBuilderABC(abc.ABC):

    @abc.abstractmethod
    def build(self) -> Tuple[str]:
        pass

    @abc.abstractmethod
    def format_url(self) -> str:
        pass
