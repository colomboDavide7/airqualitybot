#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 19:14
# @Description: this script defines a class for building postGIS consistent type to put into the queries
#
#################################################
import builtins
from typing import Dict, Any
from abc import ABC, abstractmethod
from airquality.app import EMPTY_STRING
from airquality.geom import GEO_TYPE_ST_POINT_2D


class PosGISGeomBuilder(ABC):

    EPSG_SRID = 26918

    @abstractmethod
    def build_geometry_type(self, geo_param: Dict[str, Any], geo_type: str) -> str:
        pass


    @staticmethod
    def build_ST_Point_from_coords(x: float, y: float) -> str:
        return f"ST_GeomFromText('POINT({x} {y})', {PosGISGeomBuilder.EPSG_SRID})"


    @staticmethod
    def build_ST_Point_from_geom_param(geom_param: Dict[str, Any]) -> str:
        return EMPTY_STRING




class PosGISGeomBuilderPurpleair(PosGISGeomBuilder):


    def build_geometry_type(self, geo_param: Dict[str, Any], geo_type: str) -> str:

        geo_string = EMPTY_STRING
        if not geo_param:
            return geo_string

        if "latitude" not in geo_param.keys() or "longitude" not in geo_param.keys():
            raise SystemExit(f"{PosGISGeomBuilderPurpleair.build_geometry_type.__name__}: "
                             f"missing required parameters 'latitude' or 'longitude'.")

        if geo_type == GEO_TYPE_ST_POINT_2D:
            geo_type = geo_type.format(lat = geo_param["latitude"], lon = geo_param["longitude"])
        else:
            raise SystemExit(f"{PosGISGeomBuilderPurpleair.build_geometry_type.__name__}: "
                             f"don't recognize geometry type '{geo_type}'.")

        return f"ST_GeomFromText('{geo_type}')"


################################ FACTORY ################################
class PosGISGeomBuilderFactory(builtins.object):

    @staticmethod
    def create_posGISGeomBuilder(bot_personality: str) -> PosGISGeomBuilder:
        if bot_personality == "purpleair":
            return PosGISGeomBuilderPurpleair()
        else:
            raise SystemExit(f"{PosGISGeomBuilderFactory.create_posGISGeomBuilder.__name__}: "
                             f"invalid bot personality '{bot_personality}'.")
