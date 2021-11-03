######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 16:06
# Description: this script defines a class at the head of the sqlwrapper hierarchy
#
######################################################
from abc import ABC, abstractmethod


class SQLWrapperPacket(ABC):

    @abstractmethod
    def sql(self) -> str:
        pass
