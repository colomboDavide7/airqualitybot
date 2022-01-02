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
    geolocation_record: str             # The sensor's geolocation SQL record.


@dataclass
class AddMobileMeasureResponse(object):
    """
    A *dataclass* that represents the response to a request of adding a set of mobile sensor measures.
    """

    measure_record: str                 # The sensor's measurement SQL record.


@dataclass
class AddStationMeasuresResponse(object):
    """
    A *dataclass* that represents the response to a request of adding a set of fixed sensor measures.
    """

    measure_record: str                 # The sensor's measurement SQL record.


@dataclass
class AddPlacesResponse(object):
    """
    A *dataclass* that defines the datastructure for the response to an *AddPlacesRequest* request.
    """

    place_record: str                   # The place's SQL record.
