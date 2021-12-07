######################################################
#
# Author: Davide Colombo
# Date: 07/12/21 20:16
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Generator


class FileRepoABC(abc.ABC):

    def __init__(self, path2directory: str):
        self.path2directory = path2directory

    @abc.abstractmethod
    def get_files(self) -> Generator[str, None, None]:
        pass
