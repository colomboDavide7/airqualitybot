######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 16:13
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple

POSTGIS_POINT = "POINT({lon} {lat})"
ST_GEOM_FROM_TEXT = "ST_GeomFromText('{geom}', {srid})"


@dataclass
class Geolocation(object):
    """
    A *dataclass* that holds the sensor's geolocation point.
    """

    latitude: float                     # The sensor's latitude in decimal degrees (-90,+90)
    longitude: float                    # The sensor's longitude in decimal degrees (-180,+180)
    srid: int = 26918                   # The Spatial Reference Identifier associated to the coordinate system.

    def __post_init__(self):
        if self.latitude < -90.0 or self.latitude > 90.0:
            raise ValueError(f"{type(self).__name__} expected *latitude* to be in range [-90.0 - +90.0]")
        if self.longitude < -180.0 or self.longitude > 180.0:
            raise ValueError(f"{type(self).__name__} expected *longitude* to be in range [-180.0 - +180.0]")

    @property
    def geometry_as_text(self) -> str:
        return ST_GEOM_FROM_TEXT.format(geom=self.geometry, srid=self.srid)

    @property
    def geometry(self) -> str:
        return POSTGIS_POINT.format(lon=self.longitude, lat=self.latitude)


@dataclass
class NullGeolocation(object):

    @property
    def geometry(self):
        return "NULL"

    @property
    def geometry_as_text(self) -> str:
        return "NULL"


@dataclass
class Channel(object):
    """
    A *dataclass* that holds the values of the parameters of a sensor's acquisition channel.
    """

    api_key: str                        # The API key used to access the sensor's data.
    api_id: str                         # The API identifier used to access the sensor's data.
    channel_name: str                   # The channel name given by the system to identify a sensor's channel.
    last_acquisition: datetime          # The time stamp of the last successful acquisition store in the database.


@dataclass
class AddFixedSensorRequest(object):
    """
    A *dataclass* that represents the request model for adding a new sensor.
    """

    name: str                           # The name assigned to the sensor.
    type: str                           # The type assigned to the sensor.
    channels: List[Channel]             # The API parameters of each channel associated to the sensor.
    geolocation: Geolocation            # The sensor's geolocation in decimal degrees.


@dataclass
class AddMobileMeasureRequest(object):
    """
    A *dataclass* that represents the request model for adding a new measure of a mobile sensor.
    """

    timestamp: datetime                 # The datetime object that represents the acquisition time.
    geolocation: Geolocation            # The sensor's geolocation at the moment of the acquisition in decimal degrees.
    measures: List[Tuple[int, float]]   # The collection of (param_id, param_value) tuples for each parameter.
