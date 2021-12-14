######################################################
#
# Author: Davide Colombo
# Date: 14/12/21 09:45
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc


class DBRepoABC(abc.ABC):

    @abc.abstractmethod
    def push(self, data) -> None:
        pass
