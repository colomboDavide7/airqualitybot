######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 16:13
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.datamodel.geometry import PostgisGeometry
from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple


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
class AddFixedSensorsRequest(object):
    """
    A *dataclass* that represents the request model for adding a new sensor.
    """

    name: str                           # The name assigned to the sensor.
    type: str                           # The type assigned to the sensor.
    channels: List[Channel]             # The API parameters of each channel associated to the sensor.
    geolocation: PostgisGeometry        # The sensor's geolocation in decimal degrees.


@dataclass
class AddSensorMeasuresRequest(object):
    """
    A *dataclass* that represents the request model for adding a new measure of a fixed sensor (i.e., a station).
    """

    timestamp: datetime                 # The datetime object that represents the acquisition time.
    measures: List[Tuple[int, float]]   # The collection of (param_id, param_value) tuples for each parameter.


@dataclass
class AddMobileMeasuresRequest(AddSensorMeasuresRequest):
    """
    A *dataclass* that represents the request model for adding a new measure of a mobile sensor.
    """

    geolocation: PostgisGeometry        # The sensor's geolocation at the moment of the acquisition in decimal degrees.
