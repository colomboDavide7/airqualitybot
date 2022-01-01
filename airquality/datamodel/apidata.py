######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 15:29
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from dataclasses import dataclass
from typing import Dict


@dataclass
class PurpleairAPIData(object):
    """
    A *dataclass* that represents the raw Purpleair API data of a single sensor.
    """

    name: str                           # The name assigned to a Purpleair sensor.
    sensor_index: int                   # The unique number assigned to a Purpleair sensor.
    latitude: float                     # The latitude position value for the sensor.
    longitude: float                    # The longitude position value for the sensor.
    altitude: float                     # The altitude for the sensor's location in feet.
    primary_id_a: int                   # ThingSpeak channel ID for storing sensor values.
    primary_key_a: str                  # ThingSpeak read key used for accessing data for the channel.
    primary_id_b: int                   # ThingSpeak channel ID for storing sensor values.
    primary_key_b: str                  # ThingSpeak read key used for accessing data for the channel.
    secondary_id_a: int                 # ThingSpeak channel ID for storing sensor values.
    secondary_key_a: str                # ThingSpeak read key used for accessing data for the channel.
    secondary_id_b: int                 # ThingSpeak channel ID for storing sensor values.
    secondary_key_b: str                # ThingSpeak read key used for accessing data for the channel.
    date_created: int                   # The UNIX time stamp from when the device was created.


@dataclass
class AtmotubeAPIData(object):
    """
    A *dataclass* that represents the raw Atmotube API data of a single sensor.
    """

    time: str                           # The acquisition timestamp (e.g., 2021-10-11T09:44:00.000Z).
    voc: float = None                   # The Volatile Organic Compound concentration in the air in ppm.
    pm1: int = None                     # The PM < 1.0 µm concentration in the air in µg/m^3.
    pm25: int = None                    # The PM < 2.5 µm concentration in the air in µg/m^3.
    pm10: int = None                    # The PM < 10.0 µm concentration in the air in µg/m^3.
    t: int = None                       # The air temperature in Celsius degrees.
    h: int = None                       # The relative humidity in the air in percentage.
    p: float = None                     # The atmospheric pressure in the air in millibar.
    coords: Dict[str, float] = None     # The sensor's *lat* and *lon* at acquisition time in decimal degrees.


class ThingspeakPrimaryChannelAData(object):
    """
    A *dataclass* that represents the raw Thingspeak API primary data from channel A of a single sensor.
    """

    def __init__(self, **kwargs):
        self.field1 = float(kwargs['field1'])       # The atmospheric concentration of PM 1.0 (µg/m^3).
        self.field2 = float(kwargs['field2'])       # The atmospheric concentration of PM 2.5 (µg/m^3).
        self.field3 = float(kwargs['field3'])       # The atmospheric concentration of PM 10.0 (µg/m^3).
        self.field6 = float(kwargs['field6'])       # Temperature inside the sensor housing (°F).
        self.field7 = float(kwargs['field7'])       # Relative humidity inside the sensor housing (%).
        self.created_at = kwargs['created_at']      # The acquisition timestamp (e.g., 2021-12-20T11:18:40Z).
