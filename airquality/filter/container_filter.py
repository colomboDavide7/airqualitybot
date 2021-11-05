#################################################
#
# @Author: davidecolombo
# @Date: lun, 25-10-2021, 12:20
# @Description: this script defines the classes for filtering packets coming from sensor's API based on some criteria
#
#################################################
from typing import List, Any
from abc import ABC, abstractmethod


class ContainerFilter(ABC):

    def __init__(self, filter_list: List[Any]):
        self.filter_list = filter_list

    @abstractmethod
    def filter_container(self) -> bool:
        pass


class ContainerIdentifierFilter(ContainerFilter):

    def __init__(self, filter_list: List[Any]):
        super().__init__(filter_list)

    def filter_container(self) -> bool:
        pass
