######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 05/11/21 19:09
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from abc import ABC, abstractmethod
from airquality.filter.container_filter import ContainerFilter


class FilterableContainer(ABC):

    @abstractmethod
    def apply_filter(self, container_filter: ContainerFilter):
        pass
