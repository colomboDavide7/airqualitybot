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
    Weather, WeatherForecast, OpenWeatherMapAPIData, WeatherCityData


class PurpleairAPIDataBuilder(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and defines the business rules for
    extracting the items from a PurpleAir json response.

    Keyword arguments:
        *json_response*         the json response from PurpleAir API.

    """

    def __init__(self, json_response: Dict[str, Any]):
        self._jresp = json_response
        self._fields = self._jresp['fields']
        self._data = self._jresp['data']

    def items(self) -> Generator[PurpleairAPIData, None, None]:
        return (PurpleairAPIData(**(dict(zip(self._fields, data)))) for data in self._data)


class AtmotubeAPIDataBuilder(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and defines the business rules for
    extracting the items from an Atmotube json response.

    Keyword arguments:
        *json_response*         the json response from Atmotube API.

    """

    def __init__(self, json_response: Dict[str, Any]):
        self._jresp = json_response
        self._items = self._jresp['data']['items']

    def items(self) -> Generator[AtmotubeAPIData, None, None]:
        return (AtmotubeAPIData(**item) for item in self._items)


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
        yield OpenWeatherMapAPIData(
            current=self.forecast_of(source=self.current),
            hourly_forecast=[self.forecast_of(source=item) for item in self.hourly],
            daily_forecast=[self.daily_forecast_of(source=item) for item in self.daily]
        )

    def forecast_of(self, source: Dict[str, Any]) -> WeatherForecast:
        return WeatherForecast(
            dt=self.timestamp_of(source=source),
            temp=source.get('temp'),
            pressure=source.get('pressure'),
            humidity=source.get('humidity'),
            wind_speed=source.get('wind_speed'),
            wind_deg=source.get('wind_deg'),
            weather=self.weather_of(source=source),
            rain=self.recursive_search(source=source, keywords=['rain', '1h']),
            snow=self.recursive_search(source=source, keywords=['snow', '1h']),
        )

    def daily_forecast_of(self, source: Dict[str, Any]) -> WeatherForecast:
        return WeatherForecast(
            dt=self.timestamp_of(source=source),
            temp=self.recursive_search(source=source, keywords=['temp', 'day']),
            temp_min=self.recursive_search(source=source, keywords=['temp', 'min']),
            temp_max=self.recursive_search(source=source, keywords=['temp', 'max']),
            pressure=source.get('pressure'),
            humidity=source.get('humidity'),
            wind_speed=source.get('wind_speed'),
            wind_deg=source.get('wind_deg'),
            weather=self.weather_of(source=source),
            rain=source.get('rain'),
            snow=source.get('snow')
        )

    def timestamp_of(self, source: Dict[str, Any]):
        return source['dt'] + self.tz_offset

    def weather_of(self, source: Dict[str, Any]) -> List[Weather]:
        weather = source.get('weather')
        if weather is not None:
            weather = [Weather(**w) for w in weather]
        return weather

    def recursive_search(self, source: Dict[str, Any], keywords: List[str]):
        if type(source) != dict:
            return source
        return self.recursive_search(source=source.get(keywords.pop(0)), keywords=keywords)


class WeatherCityDataBuilder(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules for reading the city data from a file and
    translate them into a Generator of *WeatherCityData* objects that are used for querying city's information
    from the *geographical_area* table in the database.
    """

    def __init__(self, filepath: str):
        with open(filepath, 'r') as f:
            parsed = loads(f.read())
            self.cities = parsed['cities']

    def items(self) -> Generator[WeatherCityData, None, None]:
        return (WeatherCityData(**city) for city in self.cities)
