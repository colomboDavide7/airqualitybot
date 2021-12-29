######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 15:29
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from dataclasses import dataclass


@dataclass
class AddPurpleairSensorRequest(object):
    """
    A *dataclass* that represents the request to add a Purpleair sensor.
    """

    name: str                       # The name assigned to a Purpleair sensor.
    sensor_index: int               # The unique number assigned to a Purpleair sensor.
    latitude: float                 # The latitude position value for the sensor.
    longitude: float                # The longitude position value for the sensor.
    altitude: float                 # The altitude for the sensor's location in feet.
    primary_id_a: int               # ThingSpeak channel ID for storing sensor values.
    primary_key_a: str              # ThingSpeak read key used for accessing data for the channel.
    primary_id_b: int               # ThingSpeak channel ID for storing sensor values.
    primary_key_b: str              # ThingSpeak read key used for accessing data for the channel.
    secondary_id_a: int             # ThingSpeak channel ID for storing sensor values.
    secondary_key_a: str            # ThingSpeak read key used for accessing data for the channel.
    secondary_id_b: int             # ThingSpeak channel ID for storing sensor values.
    secondary_key_b: str            # ThingSpeak read key used for accessing data for the channel.
    date_created: int               # The UNIX time stamp from when the device was created.


@dataclass
class AddAtmotubeMeasureRequest(object):
    """
    A *dataclass* that represents the request to add an Atmotube measure.
    """

    time: str                       # The acquisition timestamp (e.g., 2021-10-11T09:44:00.000Z)
    voc: float                      # The Volatile Organic Compound concentration in the air in ppm.
    pm1: int                        # The PM < 1.0 µm concentration in the air in µg/m^3.
    pm25: int                       # The PM < 2.5 µm concentration in the air in µg/m^3.
    pm10: int                       # The PM < 10.0 µm concentration in the air in µg/m^3.
    temperature: int                # The air temperature in Celsius degrees.
    humidity: int                   # The relative humidity in the air in percentage.
    pressure: float                 # The atmospheric pressure in the air in millibar.
    latitude: float                 # The sensor's latitude at the moment of the acquisition in decimal degrees.
    longitude: float                # The sensor's longitude at the moment of the acquisition in decimal degrees.
