######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 16:13
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.datamodel.geometry import PostgisPoint
from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple
from abc import ABC, abstractmethod


class sqlizableABC(ABC):

    @abstractmethod
    def sqlize(self) -> str:
        pass


@dataclass
class SensorChannelParam(sqlizableABC):
    """
    A *dataclass* that holds the values of the parameters of a sensor's acquisition channel.
    """

    api_key: str                        # The API key used to access the sensor's data.
    api_id: str                         # The API identifier used to access the sensor's data.
    channel_name: str                   # The channel name given by the system to identify a sensor's channel.
    last_acquisition: datetime          # The time stamp of the last successful acquisition store in the database.

    def sqlize(self) -> str:
        return f"'{self.api_key}', '{self.api_id}', '{self.channel_name}', '{self.last_acquisition}'"


@dataclass
class SensorInfo(sqlizableABC):
    name: str
    type: str

    def sqlize(self) -> str:
        return f"'{self.type}', '{self.name}'"


@dataclass
class AddFixedSensorRequest(object):
    """
    A *dataclass* that represents the request model for adding a new sensor.
    """

    basic_info: SensorInfo                      # The sensor's basic info that comprehend its name and type.
    channel_param: List[SensorChannelParam]          # The API parameters of each channel associated to the sensor.


@dataclass
class AddMobileMeasureRequest(sqlizableABC):
    """
    A *dataclass* that represents the request model for adding a new measure of a fixed sensor (i.e., a station).
    """

    timestamp: datetime                 # The datetime object that represents the acquisition time.
    measures: List[Tuple[int, float]]   # The collection of (param_id, param_value) tuples for each parameter.
    geolocation: PostgisPoint = None    # The sensor's geolocation at the moment of the acquisition in decimal degrees.

    def sqlize(self) -> str:
        return ','.join('({pid}, ' + f"{param_id}, {param_val}, '{self.timestamp}', {self.geolocation})"
                        for param_id, param_val in self.measures)


@dataclass
class AddStationMeasureRequest(sqlizableABC):
    """
    A *dataclass* that represents the request model for adding a new measure of a fixed sensor (i.e., a station).
    """

    timestamp: datetime                 # The datetime object that represents the acquisition time.
    measures: List[Tuple[int, float]]   # The collection of (param_id, param_value) tuples for each parameter.
    geolocation: PostgisPoint = None    # The sensor's geolocation at the moment of the acquisition in decimal degrees.

    def sqlize(self) -> str:
        return ','.join("({pid}, {sid}, " + f"{param_id}, {param_val}, '{self.timestamp}')"
                        for param_id, param_val in self.measures)


@dataclass
class AddPlaceRequest(sqlizableABC):
    """
    A *dataclass* that represents the datastructure of a request for adding a new place of a given country.
    """

    countrycode: str                    # The place's 2-alpha ISO country code.
    placename: str                      # The place's name.
    province: str                       # The place's province name.
    poscode: str                        # The place's postal code.
    state: str                          # The place's state name.
    geolocation: PostgisPoint           # The place's estimated geolocation

    def sqlize(self) -> str:
        return f"('{self.poscode}', '{self.countrycode}', '{self.placename}', " \
               f"'{self.province}', '{self.state}', {self.geolocation})"


@dataclass
class WeatherConditionsRequest(object):
    """
    A *dataclass* that defines the raw datastructure for the request of adding new weather conditions data.
    This class is used both for current weather, hourly forecast and daily forecast data.
    """

    timestamp: datetime                 # The datetime object that represents the forecast time (local timezone).
    weather_id: int                     # The id that identifies a row of *weather_condition* table.
    temperature: float                  # The daily temperature in °C.
    pressure: float                     # The atmospheric pressure in mbar.
    humidity: float                     # The relative humidity in %.
    wind_speed: float                   # The wind's speed in m/s.
    wind_direction: float               # The wind's direction in meteorological degrees.
    rain: float = None                  # The volume of rain precipitation in mm.
    pop: float = None                   # The probability of precipitation in %.
    snow: float = None                  # The volume of snow precipitation in mm.
    min_temp: float = None              # The daily minimum temperature in °C.
    max_temp: float = None              # The daily maximum temperature in °C.
    sunrise: datetime = None            # The datetime object that represent the sunrise time (local timezone).
    sunset: datetime = None             # The datetime object that represent the sunrise time (local timezone).


@dataclass
class WeatherAlertRequest(object):
    """
    A *dataclass* that defines the raw datastructure for a request of adding a weather alert.
    """

    sender_name: str                    # The alert's sender name.
    alert_event: str                    # The specific event for this alert.
    alert_begin: datetime               # The datetime object that represent the alert begin (local timezone).
    alert_until: datetime               # The datetime object that represent the alert end time (local timezone).
    description: str                    # The alert description.


@dataclass
class AddWeatherDataRequest(object):
    """
    A *dataclass* that defines the raw data structure for a request of adding new data fetched from OpenWeatherMap API.
    """

    current: WeatherConditionsRequest        # The request for the current weather.
    hourly: List[WeatherConditionsRequest]   # The list of requests for the hourly forecast weather (next 48 hours).
    daily: List[WeatherConditionsRequest]    # The list of requests for the daily forecast weather (next 7 days).
    alerts: List[WeatherAlertRequest]        # The list of requests of weather alert for the requested location.
