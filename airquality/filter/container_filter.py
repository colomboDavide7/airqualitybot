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

    def __init__(self, filter_list: List[Any], keep=False):
        self.filter_list = filter_list
        self.keep = keep

    @abstractmethod
    def filter_container(self, to_filter: Any) -> bool:
        pass


class ContainerIdentifierFilter(ContainerFilter):

    def __init__(self, filter_list: List[Any], keep=False):
        super().__init__(filter_list=filter_list, keep=keep)

    def filter_container(self, to_filter: Any) -> bool:
        if not self.filter_list:
            return True
        return (to_filter not in self.filter_list) ^ self.keep
