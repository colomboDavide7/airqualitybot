######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 06/11/21 19:11
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from abc import ABC, abstractmethod


class ComparableContainer(ABC):

    @abstractmethod
    def compare_to(self, container: object) -> bool:
        pass
