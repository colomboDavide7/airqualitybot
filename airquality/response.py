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


@dataclass
class Geolocation(object):
    latitude: float
    longitude: float

    def __post_init__(self):
        if self.latitude < -90.0 or self.latitude > 90.0:
            raise ValueError(f"{type(self).__name__} expected *latitude* to be in range [-90.0 - +90.0]")
        if self.longitude < -180.0 or self.longitude > 180.0:
            raise ValueError(f"{type(self).__name__} expected *longitude* to be in range [-180.0 - +180.0]")


@dataclass
class Channel(object):
    key: str
    ident: str
    name: str
    last_acquisition: datetime


@dataclass
class AddFixedSensorResponse(object):
    """
    A *dataclass* that represents the response model for adding a new sensor.
    """

    name: str                           # The name assigned to the sensor.
    type: str                           # The type assigned to the sensor.
    api_param: List[Channel]            # The API parameters of each channel associated to the sensor.
    geolocation: Geolocation            # The sensor's geolocation in decimal degrees.


@dataclass
class AddMobileMeasureResponse(object):
    """
    A *dataclass* that represents the response model for adding a new measure of a mobile sensor.
    """

    timestamp: datetime                 # The datetime object that represents the acquisition time.
    geolocation: Geolocation            # The sensor's geolocation at the moment of the acquisition in decimal degrees.
    measures: List[Tuple[int, float]]   # The collection of (param_id, param_value) tuples for each parameter.
