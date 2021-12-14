######################################################
#
# Author: Davide Colombo
# Date: 14/12/21 09:45
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc


class SQLBuilderABC(abc.ABC):

    @abc.abstractmethod
    def sql(self, data) -> str:
        pass
