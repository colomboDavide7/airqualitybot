######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 20:12
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from json import loads
from typing import Generator, Dict, List, Any
from urllib.request import urlopen
from airquality.core.iteritems import IterableItemsABC
from airquality.datamodel.apidata import PurpleairAPIData, AtmotubeAPIData, ThingspeakAPIData, GeonamesData, \
    Weather, WeatherForecast, OpenWeatherMapAPIData


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

        current = WeatherForecast(
            dt=self.timestamp_of(source=self.current),
            temp=self.current.get('temp'),
            pressure=self.current.get('pressure'),
            humidity=self.current.get('humidity'),
            wind_speed=self.current.get('wind_speed'),
            wind_deg=self.current.get('wind_deg'),
            weather=self.weather(source=self.current),
            rain=self.recursive_search(source=self.current, keywords=['rain', '1h']),
            snow=self.recursive_search(source=self.current, keywords=['snow', '1h'])
        )

        hourly_forecast = []
        for hf in self.hourly:
            hourly_forecast.append(
                WeatherForecast(
                    dt=self.timestamp_of(source=hf),
                    temp=hf.get('temp'),
                    pressure=hf.get('pressure'),
                    humidity=hf.get('humidity'),
                    wind_speed=hf.get('wind_speed'),
                    wind_deg=hf.get('wind_deg'),
                    weather=self.weather(source=hf),
                    rain=self.recursive_search(source=hf, keywords=['rain', '1h']),
                    snow=self.recursive_search(source=hf, keywords=['snow', '1h']),
                )
            )

        daily_forecast = []
        for day in self.daily:
            daily_forecast.append(
                WeatherForecast(
                    dt=self.timestamp_of(source=day),
                    temp=self.recursive_search(source=day, keywords=['temp', 'day']),
                    temp_min=self.recursive_search(source=day, keywords=['temp', 'min']),
                    temp_max=self.recursive_search(source=day, keywords=['temp', 'max']),
                    pressure=day.get('pressure'),
                    humidity=day.get('humidity'),
                    wind_speed=day.get('wind_speed'),
                    wind_deg=day.get('wind_deg'),
                    weather=self.weather(source=day),
                    rain=day.get('rain'),
                    snow=day.get('snow')
                )
            )

        yield OpenWeatherMapAPIData(
            current=current,
            hourly_forecast=hourly_forecast,
            daily_forecast=daily_forecast
        )

    def timestamp_of(self, source: Dict[str, Any]):
        return source['dt'] + self.tz_offset

    def weather(self, source: Dict[str, Any]) -> List[Weather]:
        weather = source.get('weather')
        if weather is not None:
            weather = [Weather(main=w['main'], description=w['description']) for w in weather]
        return weather

    def recursive_search(self, source: Dict[str, Any], keywords: List[str]):
        if type(source) != dict:
            return source
        return self.recursive_search(source=source.get(keywords.pop(0)), keywords=keywords)
