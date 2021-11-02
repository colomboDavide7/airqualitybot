#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 19:14
# @Description: this script defines a class for building postGIS consistent type to put into the queries
#
#################################################
import builtins
from geom.postgis_geometry import PostGISPoint
from airquality.constants.shared_constants import GEO_TYPE_ST_POINT_2D


class PostGISGeomBuilder(builtins.object):

    @classmethod
    def postgisgeom2geostring(cls, postgis_geom: PostGISPoint) -> str:

        geo_string = GEO_TYPE_ST_POINT_2D.format(lat=postgis_geom.lat, lon=postgis_geom.lng)
        return f"ST_GeomFromText('{geo_string}')"

    @classmethod
    def extract_geotype_from_geostring(cls, geo_string: str) -> str:
        substring = geo_string[geo_string.find("'") + 1:]
        return substring[:substring.find("'")]
