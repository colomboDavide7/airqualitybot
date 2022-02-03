# ======================================
# @author:  Davide Colombo
# @date:    2022-01-30, dom, 16:54
# ======================================
from abc import ABC, abstractmethod


class UsecaseABC(ABC):

    @abstractmethod
    def execute(self):
        pass
