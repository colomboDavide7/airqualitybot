######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 06/11/21 09:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from abc import ABC, abstractmethod


class IdentifiableContainer(ABC):

    @abstractmethod
    def identifier(self) -> str:
        pass
