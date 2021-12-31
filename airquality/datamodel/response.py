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
    A *dataclass* that represents the response to a request of adding a mobile sensor's measure.
    """

    measure_record: str                 # The sensor's measurement SQL record.
