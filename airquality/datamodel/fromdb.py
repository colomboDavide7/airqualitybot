# ======================================
# @author:  Davide Colombo
# @date:    2022-02-2, mer, 12:35
# ======================================
from typing import Tuple


class GeoareaLocationDM(object):
    """
    A class that defines the raw datastructure for the database information of a city.
    """

    def __init__(self, row: Tuple):
        self._geoarea_id = row[0]
        self._longitude = row[1]
        self._latitude = row[2]

    @property
    def latitude(self) -> float:
        return self._latitude

    @property
    def longitude(self) -> float:
        return self._longitude

    @property
    def geoarea_id(self) -> int:
        return self._geoarea_id

    def __repr__(self):
        return f"{type(self).__name__}(geoarea_id={self._geoarea_id}, " \
               f"longitude={self._longitude}, latitude={self._latitude})"
