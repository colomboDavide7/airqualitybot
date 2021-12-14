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


RESPONSE_TYPE = Generator[linetype.GeoareaLineTypeABC, None, None]


# ------------------------------- GeoareaFilter ------------------------------- #
class GeoareaFilter(datafilter.FilterABC):

    def __init__(self, places: List[str], postalcodes: List[str] = ()):
        super(GeoareaFilter, self).__init__()
        self._target_postalcodes = postalcodes
        self._known_places = places

    ################################ filter() ################################
    def filter(self, all_lines: RESPONSE_TYPE) -> RESPONSE_TYPE:
        new_places = self.new_places(all_lines)
        if self._target_postalcodes:
            return self.search_postalcodes(new_places)
        return new_places

    ################################ new_places() ################################
    def new_places(self, lines: RESPONSE_TYPE) -> RESPONSE_TYPE:
        for line in lines:
            if line.place_name() not in self._known_places:
                yield line

    ################################ search_postalcodes() ################################
    def search_postalcodes(self, lines: RESPONSE_TYPE) -> RESPONSE_TYPE:
        for line in lines:
            if line.postal_code() in self._target_postalcodes:
                yield line
