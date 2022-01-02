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


class ThingspeakAPIData(object):
    """
    A *dataclass* that represents the raw Thingspeak API data of a single sensor.
    This class is used as a template for all the channels of the sensor.

    Primary Channel A:
    *field1* => The atmospheric concentration of PM 1.0 (µg/m^3).
    *field2* => The atmospheric concentration of PM 2.5 (µg/m^3).
    *field3* => The atmospheric concentration of PM 1.0 (µg/m^3).
    *field6* => Temperature inside the sensor housing (°F).
    *field7* => Relative humidity inside the sensor housing (%).

    Primary Channel B:
    *field1* => The atmospheric concentration of PM 1.0 (µg/m^3).
    *field2* => The atmospheric concentration of PM 2.5 (µg/m^3).
    *field3* => The atmospheric concentration of PM 1.0 (µg/m^3).
    *field6* => The current pressure in Millibars.

    Secondary Channel A:
    *field1* => Count concentration (particles/100ml) of all particles greater than 0.3 µm diameter.
    *field2* => Count concentration (particles/100ml) of all particles greater than 0.5 µm diameter.
    *field3* => Count concentration (particles/100ml) of all particles greater than 1.0 µm diameter.
    *field4* => Count concentration (particles/100ml) of all particles greater than 2.5 µm diameter.
    *field5* => Count concentration (particles/100ml) of all particles greater than 5.0 µm diameter.
    *field6* => Count concentration (particles/100ml) of all particles greater than 10.0 µm diameter.

    Secondary Channel B:
    *field1* => Count concentration (particles/100ml) of all particles greater than 0.3 µm diameter.
    *field2* => Count concentration (particles/100ml) of all particles greater than 0.5 µm diameter.
    *field3* => Count concentration (particles/100ml) of all particles greater than 1.0 µm diameter.
    *field4* => Count concentration (particles/100ml) of all particles greater than 2.5 µm diameter.
    *field5* => Count concentration (particles/100ml) of all particles greater than 5.0 µm diameter.
    *field6* => Count concentration (particles/100ml) of all particles greater than 10.0 µm diameter.

    """

    def __init__(self, **kwargs):
        self.field1 = None if kwargs.get('field1') is None else float(kwargs.get('field1'))
        self.field2 = None if kwargs.get('field2') is None else float(kwargs.get('field2'))
        self.field3 = None if kwargs.get('field3') is None else float(kwargs.get('field3'))
        self.field4 = None if kwargs.get('field4') is None else float(kwargs.get('field4'))
        self.field5 = None if kwargs.get('field5') is None else float(kwargs.get('field5'))
        self.field6 = None if kwargs.get('field6') is None else float(kwargs.get('field6'))
        self.field7 = None if kwargs.get('field7') is None else float(kwargs.get('field7'))
        self.created_at = kwargs['created_at']


@dataclass
class GeonamesData(object):

    def __init__(self, *args):
        self.country_code = args[0]
        self.postal_code = args[1]
        self.place_name = args[2].replace("'", "")
        self.state = args[3].replace("'", "")
        self.province = args[5].replace("'", "")
        self.latitude = float(args[9])
        self.longitude = float(args[10])
