######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 19:28
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from dataclasses import dataclass


class NullGeometry(object):
    """
    An object that represents the SQL value for a NULL geometry.
    """

    def __str__(self):
        return 'NULL'


@dataclass
class PostgisPoint(object):
    """
    An object that represents the SQL value for a PostGIS point.
    """

    latitude: float                     # The latitude value in decimal degrees (-90,+90)
    longitude: float                    # The longitude value in decimal degrees (-180,+180)
    srid: int = 4326                    # The Spatial Reference System Identifier (default is WGS84)

    def __post_init__(self):
        if self.latitude < -90.0 or self.latitude > 90.0:
            raise ValueError(f"{type(self).__name__} expected *latitude* to be in range [-90.0 - +90.0]")
        if self.longitude < -180.0 or self.longitude > 180.0:
            raise ValueError(f"{type(self).__name__} expected *longitude* to be in range [-180.0 - +180.0]")

    def __str__(self):
        geom = f"POINT({self.longitude} {self.latitude})"
        return f"ST_GeomFromText('{geom}', {self.srid})"
