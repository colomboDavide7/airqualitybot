######################################################
#
# Author: Davide Colombo
# Date: 07/12/21 20:16
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Tuple
import airquality.logger.loggable as log


# ------------------------------- FileRepoABC ------------------------------- #
class FileRepoABC(log.Loggable, abc.ABC):

    @abc.abstractmethod
    def read_all(self) -> Tuple[str]:
        pass

    @abc.abstractmethod
    def read_file(self, filename: str) -> str:
        pass
