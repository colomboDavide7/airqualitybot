#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 19:14
# @Description: this script defines a class for building postGIS consistent type to put into the queries
#
#################################################
import builtins
from typing import Dict, Any
from airquality.constants.shared_constants import EMPTY_STRING, EMPTY_DICT, \
    GEO_TYPE_ST_POINT_2D, GEOMBUILDER_LATITUDE, GEOMBUILDER_LONGITUDE


class PostGISGeomBuilder(builtins.object):

    @classmethod
    def build_geometry_type(cls, geo_param: Dict[str, Any], geo_type: str) -> str:
        """Class method that takes a set of geometry parameters (latitude, longitude) and a geometry type string
        and returns a string for building the respective PostGIS geometry type."""

        geo_string = EMPTY_STRING
        if geo_param == EMPTY_DICT:
            return geo_string

        if GEOMBUILDER_LATITUDE not in geo_param.keys() or GEOMBUILDER_LONGITUDE not in geo_param.keys():
            raise SystemExit(f"{PostGISGeomBuilder.build_geometry_type.__name__}: "
                             f"missing required parameters (GEOMBUILDER_LATITUDE | GEOMBUILDER_LONGITUDE).")

        if geo_type == GEO_TYPE_ST_POINT_2D:
            geo_string = geo_type.format(lat = geo_param[GEOMBUILDER_LATITUDE], lon = geo_param[GEOMBUILDER_LONGITUDE])
        else:
            raise SystemExit(f"{PostGISGeomBuilder.build_geometry_type.__name__}: "
                             f"don't recognize geometry type '{geo_type}'.")

        return f"ST_GeomFromText('{geo_string}')"
