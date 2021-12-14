######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 17:27
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Generator, List
import airquality.filter.abc as datafilter
import airquality.file.line.abc as linetype


# ------------------------------- GeoareaFilter ------------------------------- #
class GeoareaFilter(datafilter.FilterABC):

    def __init__(self, postalcodes: List[str] = (), places: List[str] = (), only_unique_lines=True):
        super(GeoareaFilter, self).__init__()
        self.only_unique_lines = only_unique_lines
        self._postalcode2keep = postalcodes
        self._database_place_names = places

    ################################ filter() ################################
    def filter(self, all_resp: Generator[linetype.GeoareaLineTypeABC, None, None]) -> Generator[linetype.GeoareaLineTypeABC, None, None]:
        new_places = self.new_places(all_resp)
        if self._postalcode2keep:
            return self.patient_postalcodes(new_places)
        return new_places

    ################################ new_places() ################################
    def new_places(
            self, resp2filter: Generator[linetype.GeoareaLineTypeABC,  None, None]
    ) -> Generator[linetype.GeoareaLineTypeABC,  None, None]:
        for line in resp2filter:
            if line.place_name() not in self._database_place_names:
                yield line

    ################################ patient_postalcodes() ################################
    def patient_postalcodes(
            self, resp2filter: Generator[linetype.GeoareaLineTypeABC,  None, None]
    ) -> Generator[linetype.GeoareaLineTypeABC,  None, None]:
        for line in resp2filter:
            if line.postal_code() in self._postalcode2keep:
                yield line
