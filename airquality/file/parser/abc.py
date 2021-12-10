######################################################
#
# Author: Davide Colombo
# Date: 10/12/21 16:27
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc


class FileParserABC(abc.ABC):

    @abc.abstractmethod
    def parse(self, text: str):
        pass
