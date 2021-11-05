######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 05/11/21 11:19
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from abc import ABC, abstractmethod


class Container2SQL(ABC):

    @abstractmethod
    def container2sql(self) -> str:
        pass
