######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 15:29
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class PurpleairDM(object):
    """
    A *dataclass* that represents the raw Purpleair API data of a single sensor.
    """

    name: str                           # The name assigned to a Purpleair sensor.
    latitude: float                     # The latitude position value for the sensor.
    longitude: float                    # The longitude position value for the sensor.
    sensor_index: int                   # The unique number assigned to a Purpleair sensor.
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
class AtmotubeDM(object):
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


class ThingspeakDM(object):
    """
    A *dataclass* that represents the raw Thingspeak API data of a single sensor.
    This class is used as a template for all the channels of the sensor.

    Primary Channel A:
    *field1* => The atmospheric concentration of PM 1.0 (µg/m^3).
    *field2* => The atmospheric concentration of PM 2.5 (µg/m^3).
    *field3* => The atmospheric concentration of PM 10.0 (µg/m^3).
    *field6* => Temperature inside the sensor housing (°F).
    *field7* => Relative humidity inside the sensor housing (%).

    Primary Channel B:
    *field1* => The atmospheric concentration of PM 1.0 (µg/m^3).
    *field2* => The atmospheric concentration of PM 2.5 (µg/m^3).
    *field3* => The atmospheric concentration of PM 10.0 (µg/m^3).
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
class WeatherDM(object):
    """
    A *dataclass* that defines the raw datastructure of the weather conditions in a *WeatherForecast* object.
    """

    id: int                                       # The weather condition code.
    icon: str                                       # The weather condition icon name.
    main: str                                       # The weather condition name.
    description: str                                # The description of the weather condition above.


@dataclass
class WeatherAlertDM(object):
    """
    A dataclass that defines the raw datastructure for openweathermap.org weather alerts.
    """

    sender_name: str                                # The name of the alert source.
    alert_event: str                                # The alert event name.
    alert_begin: int                                # The UNIX time stamp from which the alert begins (UTC).
    alert_until: int                                # The UNIX time stamp until the alert is valid (UTC).
    description: str                                # The alert long description.


@dataclass
class WeatherConditionsDM(object):
    """
    A *dataclass* that defines the raw datastructure of the weather forecast conditions.
    """

    dt: int                                         # The UNIX time stamp at acquisition time (UTC).
    temp: float                                     # The daily temperature conditions for this forecast.
    pressure: float                                 # The pressure conditions for this forecast (mbar).
    humidity: float                                 # The humidity conditions for this forecast (%).
    wind_speed: float                               # The wind's speed in for this forecast (m/s).
    wind_deg: float                                 # The wind's direction for this forecast (degrees, °).
    weather: List[WeatherDM]                        # The list of weather conditions for this forecast.
    rain: float = None                              # The rain volume for last hour (mm).
    pop: float = None                               # The probability of precipitation (%).
    snow: float = None                              # The snow volume for last hour (mm).
    temp_min: float = None                          # The minimum temperature of the day (°C)
    temp_max: float = None                          # The maximum temperature of the day (°C)
    sunrise: int = None                             # The UNIX time stamp of the sunrise time (UTC).
    sunset: int = None                              # The UNIX time stamp of the sunset time (UTC).


@dataclass
class OpenweathermapDM(object):
    """
    A *dataclass* that defines the raw datastructure of a One Call API response available on OpenWeatherMap service.
    """

    tz_name: str                                    # The timezone name of the request location.
    current: WeatherConditionsDM                    # The current weather conditions.
    hourly_forecast: List[WeatherConditionsDM]      # The weather conditions forecast for the next 48 hours (hourly).
    daily_forecast: List[WeatherConditionsDM]       # The weather conditions forecast for the next 7 days (daily).
    alerts: List[WeatherAlertDM]                    # The weather alerts (if any) for the requested location.
