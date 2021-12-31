######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 11:29
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from collections.abc import Iterable
from abc import abstractmethod
from itertools import islice


class IterableItemsABC(Iterable):
    """
    An *Iterable* that defines the business rules for iterating over a set of *items*.
    """

    @abstractmethod
    def items(self):
        pass

    def __getitem__(self, index):
        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError(f"{type(self).__name__} expected '{index}' to be in [0 - {len(self)}]")
        return next(islice(self, index, None))

    def __iter__(self):
        return self.items()

    def __len__(self):
        return sum(1 for _ in self.items())
