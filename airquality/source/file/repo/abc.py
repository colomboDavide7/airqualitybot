######################################################
#
# Author: Davide Colombo
# Date: 07/12/21 20:16
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Generator


# ------------------------------- FileRepoABC ------------------------------- #
class FileRepoABC(abc.ABC):

    @abc.abstractmethod
    def get_files(self) -> Generator[str, None, None]:
        pass
