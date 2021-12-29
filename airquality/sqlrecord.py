######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 18:12
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from dataclasses import dataclass


@dataclass
class FixedSensorSQLRecord(object):
    """
    A *dataclass* that represents a fixed sensor (i.e., a station) database record.
    """

    sensor_record: str                  # The sensor's basic information SQL record.
    apiparam_record: str                # The sensor's API parameters SQL record.
    geolocation_record: str             # The sensor's geolocation SQL record.


@dataclass
class MobileMeasureSQLRecord(object):
    """
    A *dataclass* that represents a mobile sensor acquisition database record.
    """

    measure_record: str                 # The sensor's measurement SQL record.
