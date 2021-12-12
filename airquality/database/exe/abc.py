######################################################
#
# Author: Davide Colombo
# Date: 11/12/21 20:19
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc


class QueryExecutorABC(abc.ABC):

    @abc.abstractmethod
    def execute(self, data) -> None:
        pass
