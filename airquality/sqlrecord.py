######################################################
#
# Author: Davide Colombo
# Date: 24/12/21 16:34
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Generator, Dict
from airquality.iterabc import IterableItemsABC
from airquality.sqlitem import PurpleairSQLItem, AtmotubeSQLItem


class PurpleairSQLRecords(IterableItemsABC):

    def __init__(self, responses: IterableItemsABC, item_factory=PurpleairSQLItem):
        self.responses = responses
        self.item_factory = item_factory

    def items(self) -> Generator[PurpleairSQLItem, None, None]:
        return (self.item_factory(item) for item in self.responses)


class AtmotubeSQLRecords(IterableItemsABC):

    def __init__(self, responses: IterableItemsABC, measure_param: Dict[str, int], item_factory=AtmotubeSQLItem):
        self.responses = responses
        self.item_factory = item_factory
        self.measure_param = measure_param

    def items(self) -> Generator[AtmotubeSQLItem, None, None]:
        return (self.item_factory(item=item, measure_param=self.measure_param) for item in self.responses)
