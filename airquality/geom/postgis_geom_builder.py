#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 19:14
# @Description: this script defines a class for building postGIS consistent type to put into the queries
#
#################################################
import builtins


class PostGISGeomBuilder(builtins.object):

    EPSG_SRID = 26918

    @staticmethod
    def build_ST_Point_from_coords(x: float, y: float) -> str:
        return f"ST_GeomFromText('POINT({x} {y})', {PostGISGeomBuilder.EPSG_SRID})"
