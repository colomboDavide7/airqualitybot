######################################################
#
# Author: Davide Colombo
# Date: 08/12/21 14:27
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc


class SourceABC(abc.ABC):

    @abc.abstractmethod
    def get(self):
        pass
