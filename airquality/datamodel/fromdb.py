# ======================================
# @author:  Davide Colombo
# @date:    2022-02-2, mer, 12:35
# ======================================
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SensorApiParamDM(object):
    """
    An *dataclass* that represents the sensor's API parameters data queried from the database.
    """

    sensor_id: int                      # The unique identifier of a sensor within the database.
    api_key: str                        # The API key used to claim the ownership of the sensor when accessing data.
    api_id: str                         # The API id used together with the API key.
    ch_name: str                        # The name assigned to the channel associated to the API credentials.
    last_acquisition: datetime          # The timestamp of the last acquisition on the current channel.


@dataclass
class SensorLocationDM(object):
    """
    A class that defines the datastructure for a raw geolocation instance.
    """

    sensor_id: int
    latitude: float
    longitude: float


@dataclass
class OpenweathermapKeyDM(object):
    """
    A *dataclass* that defines the raw datastructure for the openweathermap API key queried from the database.
    """

    key_value: str                      # The openweathermap's API key.
    done_requests_per_minute: int       # The number of requests in the last minute done using this key.
    max_requests_per_minute: int        # The maximum number of requests that can be done in a minute.


@dataclass
class SensorInfoDM(object):
    """
    A *dataclass* that defines the raw datastructure for the sensor's basic information queried from the database.
    """

    sensor_id: int                      # The sensor's unique id.
    sensor_name: str                    # The sensor's name.
    sensor_lng: float = None            # The sensor's longitude (only if the sensor is 'fixed')
    sensor_lat: float = None            # The sensor's latitude (only if the sensor is 'fixed')


@dataclass
class GeoareaLocationDM(object):
    """
    A *dataclass* that defines the raw datastructure for the database information of a city.
    """

    geoarea_id: int                     # the place's unique ID into the 'level0_raw.geographical_area' table.
    latitude: float                     # the place's latitude in decimal degrees.
    longitude: float                    # the place's longitude in decimal degrees.
