######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 11:10
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.datamodel.request import AddFixedSensorRequest, AddMobileMeasureRequest
from airquality.core.iteritems import IterableItemsABC
from typing import Generator, Set
from datetime import datetime


class AddFixedSensorRequestValidator(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules for
    validating a set of *AddFixedSensorRequest* items.

    Only the requests whose *name* is not in *existing_names* are kept.
    """

    def __init__(self, request: IterableItemsABC, existing_names: Set[str]):
        self.request = request
        self.existing_names = existing_names

    def items(self) -> Generator[AddFixedSensorRequest, None, None]:
        for request in self.request:
            if request.name not in self.existing_names:
                yield request


class AddMobileMeasureRequestValidator(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules for
    validating a set of *AddMobileMeasureRequest* items.

    Only the requests whose *timestamp* is after the *filter_ts* are kept.
    """

    def __init__(self, request: IterableItemsABC, filter_ts: datetime):
        self.request = request
        self.filter_ts = filter_ts

    def items(self) -> Generator[AddMobileMeasureRequest, None, None]:
        for request in self.request:
            if request.timestamp > self.filter_ts:
                yield request
