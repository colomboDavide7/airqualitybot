######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 17:27
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Generator
import airquality.logger.util.decorator as log_decorator
import airquality.filter.basefilt as flt
import airquality.types.geonames as linetype


class LineFilter(flt.BaseFilter):

    def __init__(self, log_filename="log"):
        super(LineFilter, self).__init__(log_filename=log_filename)
        self.database_place_names = None

    def with_database_place_names(self, place_names: List[str]):
        self.database_place_names = place_names

    @log_decorator.log_decorator()
    def filter(self, resp2filter: Generator[linetype.GeonamesLine,  None, None]) -> Generator[linetype.GeonamesLine,  None, None]:
        if self.database_place_names is None:
            raise SystemExit(f"{LineFilter.__name__}: bad setup => missing required dependencies 'database_place_names'")

        all_responses = len(resp2filter)

        count = 0
        item_idx = 0
        place_names_with_more_than_one_occurrences = []
        while count < all_responses:
            if resp2filter[item_idx].place_name in place_names_with_more_than_one_occurrences:
                del resp2filter[item_idx]
            else:
                place_names_with_more_than_one_occurrences.append(resp2filter[item_idx].place_name)
                item_idx += 1
            count += 1
        self.log_info(f"{LineFilter.__name__}: found {len(resp2filter)}/{all_responses} unique places")
        all_responses = len(resp2filter)
        if place_names_with_more_than_one_occurrences:
            del place_names_with_more_than_one_occurrences

        count = 0
        item_idx = 0
        while count < all_responses:
            if resp2filter[item_idx].place_name in self.database_place_names:
                del resp2filter[item_idx]
            else:
                item_idx += 1
            count += 1

        self.log_info(f"{LineFilter.__name__}: found {len(resp2filter)}/{all_responses} new places")
        return resp2filter
