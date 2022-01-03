######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 20:12
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from json import loads
from typing import Generator
from urllib.request import urlopen
from airquality.core.iteritems import IterableItemsABC
from airquality.datamodel.apidata import PurpleairAPIData, AtmotubeAPIData, ThingspeakAPIData, GeonamesData, \
    Weather, Temperature, WeatherForecast, OpenWeatherMapAPIData


class PurpleairAPIDataBuilder(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules
    for fetching data from Purpleair API and build a
    generator of *PurpleairAPIData*.
    """

    def __init__(self, url: str):
        with urlopen(url) as http_response:
            parsed = loads(http_response.read())
            self.fields = parsed['fields']
            self.data = parsed['data']

    def items(self) -> Generator[PurpleairAPIData, None, None]:
        return (PurpleairAPIData(**(dict(zip(self.fields, data)))) for data in self.data)


class AtmotubeAPIDataBuilder(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules
    for fetching data from Atmotube API and build a
    generator of *AtmotubeAPIData*.
    """

    def __init__(self, url: str):
        with urlopen(url) as http_response:
            parsed = loads(http_response.read())
            self.api_items = parsed['data']['items']

    def items(self) -> Generator[AtmotubeAPIData, None, None]:
        return (AtmotubeAPIData(**item) for item in self.api_items)


class ThingspeakAPIDataBuilder(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules
    for fetching data from Thingspeak API and build a
    generator of *ThingspeakPrimaryChannelAData*.
    """

    def __init__(self, url: str):
        with urlopen(url) as http_response:
            parsed = loads(http_response.read())
            self.feeds = parsed['feeds']

    def items(self) -> Generator[ThingspeakAPIData, None, None]:
        return (ThingspeakAPIData(**item) for item in self.feeds)


class GeonamesDataBuilder(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules
    for reading geonames data from *filename* and build a
    generator of *GeonamesData*.
    """
    def __init__(self, filepath: str):
        with open(filepath, "r") as f:
            lines = f.read().split('\n')
            self.tokenized = [line.split('\t') for line in lines if line]

    def items(self) -> Generator[GeonamesData, None, None]:
        return (GeonamesData(*line) for line in self.tokenized)


class OpenWeatherMapAPIDataBuilder(IterableItemsABC):

    def __init__(self, url: str):
        with urlopen(url) as http_response:
            parsed = loads(http_response.read())
            self.tz_offset = parsed['timezone_offset']
            self.current = parsed['current']
            self.hourly = parsed['hourly']
            self.daily = parsed['daily']

    def items(self) -> Generator[OpenWeatherMapAPIData, None, None]:
        current_weather = self.current.get('weather')
        if current_weather is not None:
            current_weather = [Weather(main=w['main'], description=w['description']) for w in current_weather]

        current_rain = self.current.get('rain')
        if current_rain is not None:
            current_rain = current_rain['1h']

        current_snow = self.current.get('snow')
        if current_snow is not None:
            current_snow = current_snow['1h']

        current = WeatherForecast(
            dt=self.current['dt'] + self.tz_offset,
            temp=Temperature(day=self.current.get('temp')),
            pressure=self.current.get('pressure'),
            humidity=self.current.get('humidity'),
            wind_speed=self.current.get('wind_speed'),
            wind_deg=self.current.get('wind_deg'),
            weather=current_weather,
            rain=current_rain,
            snow=current_snow
        )

        hourly_forecast = []
        for hf in self.hourly:
            weather = hf.get('weather')
            if weather is not None:
                weather = [Weather(main=w['main'], description=w['description']) for w in weather]

            rain = hf.get('rain')
            if rain is not None:
                rain = rain['1h']

            snow = hf.get('snow')
            if snow is not None:
                snow = snow['1h']

            hourly_forecast.append(
                WeatherForecast(
                    dt=hf['dt'] + self.tz_offset,
                    temp=Temperature(day=hf.get('temp')),
                    pressure=hf.get('pressure'),
                    humidity=hf.get('humidity'),
                    wind_speed=hf.get('wind_speed'),
                    wind_deg=hf.get('wind_deg'),
                    weather=weather,
                    rain=rain,
                    snow=snow
                )
            )

        daily_forecast = []
        for day in self.daily:

            temp = day.get('temp')
            if temp is not None:
                temp = Temperature(day=temp['day'], min=temp['min'], max=temp['max'])

            weather = day.get('weather')
            if weather is not None:
                weather = [Weather(main=w['main'], description=w['description']) for w in weather]

            daily_forecast.append(
                WeatherForecast(
                    dt=day['dt'] + self.tz_offset,
                    temp=temp,
                    pressure=day.get('pressure'),
                    humidity=day.get('humidity'),
                    wind_speed=day.get('wind_speed'),
                    wind_deg=day.get('wind_deg'),
                    weather=weather,
                    rain=day.get('rain'),
                    snow=day.get('snow')
                )
            )

        yield OpenWeatherMapAPIData(
            current=current,
            hourly_forecast=hourly_forecast,
            daily_forecast=daily_forecast
        )
