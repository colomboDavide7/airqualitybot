######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 18:12
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from dataclasses import dataclass


@dataclass
class AddFixedSensorResponse(object):
    """
    A *dataclass* that represents the response to a request of adding a fixed sensor (i.e., a station).
    """

    sensor_record: str                  # The sensor's basic information SQL record.
    apiparam_record: str                # The sensor's API parameters SQL record.


@dataclass
class AddSensorMeasureResponse(object):
    """
    A *dataclass* that represents the response to a request of adding sensor measures.
    """

    measure_record: str                 # The sensor's measurement SQL record.


@dataclass
class AddPlaceResponse(object):
    """
    A *dataclass* that defines the datastructure for the response to an *AddPlaceRequest* request.
    """

    place_record: str                   # The place's SQL record inserted into 'level0_raw.geographical_area'.


@dataclass
class AddWeatherDataResponse(object):
    """
    A *dataclass* that defines the raw datastructure for the response to a request of adding OpenWeatherMap data.
    """

    current_weather_record: str         # The current weather SQL record.
    hourly_forecast_record: str         # The next 48 hours weather forecast SQL record.
    daily_forecast_record: str          # The next 7 days weather forecast SQL record.
    weather_alert_record: str           # The weather alert SQL record.
