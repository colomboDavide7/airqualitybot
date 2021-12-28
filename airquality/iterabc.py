######################################################
#
# Author: Davide Colombo
# Date: 28/12/21 20:08
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from collections.abc import Iterable
from abc import abstractmethod
from itertools import islice


class IterableItemsABC(Iterable):

    @abstractmethod
    def items(self):
        pass

    def __getitem__(self, index):
        """
        The *index* is first sum to *len(self)* to make it positive and then checked for the range validity.
        The positive index is required by *islice* function.
        """

        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError(f"{type(self).__name__} in __getitem__(): index '{index}' out of range")
        return next(islice(self, index, None))

    def __iter__(self):
        return self.items()

    def __len__(self):
        return sum(1 for _ in self.items())
