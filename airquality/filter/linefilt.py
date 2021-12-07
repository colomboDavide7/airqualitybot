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
        self.postalcode2keep = None

    def with_database_place_names(self, place_names: List[str]):
        self.database_place_names = place_names

    def with_postal_code2keep(self, postal_codes: List[str]):
        self.postalcode2keep = postal_codes

    @log_decorator.log_decorator()
    def filter(self, resp2filter: Generator[linetype.GeonamesLine,  None, None]) -> Generator[linetype.GeonamesLine,  None, None]:
        if self.database_place_names is None:
            raise SystemExit(f"{LineFilter.__name__}: bad setup => missing required dependencies 'database_place_names'")

        if self.postalcode2keep is not None:
            resp2filter = self.keep_postalcodes(resp2filter)

        for line in self.uniques(resp2filter):
            if line.place_name not in self.database_place_names:
                yield line

    @log_decorator.log_decorator()
    def uniques(self, resp2filter: Generator[linetype.GeonamesLine, None, None]) -> Generator[linetype.GeonamesLine, None, None]:
        places_with_more_than_one_occurrence = set()
        for response in resp2filter:
            if response.place_name not in places_with_more_than_one_occurrence:
                yield response
                places_with_more_than_one_occurrence.add(response.place_name)

    @log_decorator.log_decorator()
    def keep_postalcodes(self, resp2filter: Generator[linetype.GeonamesLine, None, None]) -> Generator[linetype.GeonamesLine, None, None]:
        for response in resp2filter:
            if response.postal_code in self.postalcode2keep:
                yield response
