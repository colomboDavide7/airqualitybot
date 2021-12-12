######################################################
#
# Author: Davide Colombo
# Date: 11/12/21 20:19
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc


class RecordTypeABC(abc.ABC):
    pass


class RecordBuilderABC(abc.ABC):

    @abc.abstractmethod
    def build(self, data):
        pass
