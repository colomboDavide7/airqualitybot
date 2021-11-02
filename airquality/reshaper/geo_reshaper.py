######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 12:52
# Description: this script defines a class for reshaping geometry parameters from the API into a new object
#
######################################################
import builtins
from typing import List, Dict, Any
from abc import ABC, abstractmethod
from geom.postgis_geometry import PostGISGeometry
from airquality.constants.shared_constants import EMPTY_LIST

class GeoReshaper(ABC):

    @abstractmethod
    def reshape(self, packets: List[Dict[str, Any]]) -> List[PostGISGeometry]:
        pass


class GeoReshaperPurpleair(GeoReshaper):

    def reshape(self, packets: List[Dict[str, Any]]) -> List[PostGISGeometry]:

        if packets == EMPTY_LIST:
            return []

        reshaped_packets = []
        for packet in packets:
            if


class GeoReshaperFactory(builtins.object):

    @classmethod
    def create_geo_reshaper(cls, bot_personality: str) -> GeoReshaper:

        if bot_personality == "purpleair":
            return GeoReshaperPurpleair()
        else:
            raise SystemExit(f"{GeoReshaperFactory.__name__}: cannot instantiate {GeoReshaper.__name__} "
                             f"instance for personality='{bot_personality}'."))
