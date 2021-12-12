######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 17:27
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Generator, List
import airquality.logger.util.decorator as log_decorator
import airquality.filter.abc as datafilter
import airquality.types.line.line as linetype


class GeonamesFilter(datafilter.FilterABC):

    def __init__(self, log_filename="log"):
        super(GeonamesFilter, self).__init__(log_filename=log_filename)
        self._postalcode2keep = []
        self._database_place_names = []

    def with_database_place_names(self, places: List[str]):
        self._database_place_names = places
        return self

    def with_postalcodes(self, poscodes: List[str]):
        self._postalcode2keep = poscodes
        return self

    @log_decorator.log_decorator()
    def filter(self, all_resp: Generator[linetype.GeonamesLine, None, None]) -> Generator[linetype.GeonamesLine, None, None]:
        new_places = self.new_places(all_resp)
        if self._postalcode2keep:
            return self.patient_postalcodes(new_places)
        return new_places

    def new_places(self, resp2filter: Generator[linetype.GeonamesLine,  None, None]) -> Generator[linetype.GeonamesLine,  None, None]:
        for line in resp2filter:
            if line.place_name not in self._database_place_names:
                yield line

    def patient_postalcodes(self, resp2filter: Generator[linetype.GeonamesLine,  None, None]) -> Generator[linetype.GeonamesLine,  None, None]:
        for line in resp2filter:
            if line.postal_code in self._postalcode2keep:
                yield line
