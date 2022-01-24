######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 20:12
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from json import loads
from typing import Generator, Dict, List, Any
from airquality.core.iteritems import IterableItemsABC
from airquality.datamodel.apidata import PurpleairAPIData, AtmotubeAPIData, ThingspeakAPIData, GeonamesData, \
    Weather, WeatherForecast, OpenWeatherMapAPIData, WeatherCityData, WeatherAlert


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
    A class that implements the *IterableItemsABC* interface and defines the business rules for
    extracting the items from a Thingspeak json response.

    Keyword arguments:
        *json_response*         the json response from Thingspeak API.

    """

    def __init__(self, json_response: Dict[str, Any]):
        self._jresp = json_response
        self._feeds = self._jresp['feeds']

    def items(self) -> Generator[ThingspeakAPIData, None, None]:
        return (ThingspeakAPIData(**item) for item in self._feeds)


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


def _weather_alert_datamodel(source: Dict[str, Any]) -> WeatherAlert:
    return WeatherAlert(
        sender_name=source['sender_name'],
        alert_event=source['event'],
        alert_begin=source['start'],
        alert_until=source['end'],
        description=source['description']
    )


def _weather_of(source: Dict[str, Any]) -> List[Weather]:
    weather = source.get('weather')
    if weather is not None:
        weather = [Weather(**w) for w in weather]
    return weather


class OpenWeatherMapAPIDataBuilder(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and defines the business rules for
    extracting current weather, hourly forecast and daily forecast items from an OpenWeatherMap response.

    Keyword arguments:
        *json_response*         the json response from OneCallAPI service of OpenWeatherMap.

    """

    def __init__(self, json_response: Dict[str, Any]):
        self._jresp = json_response
        self.tzname = self._jresp['timezone']               # the time zone name for the requested location.
        self.current = self._jresp['current']               # the current weather dict.
        self.hourly = self._jresp['hourly']                 # the list of hourly weather forecast.
        self.daily = self._jresp['daily']                   # the list of daily weather forecast.
        self._alerts = self._jresp.get('alerts', ())        # the list of weather alerts (DEFAULTS TO EMPTY LIST !!!)

    def items(self) -> Generator[OpenWeatherMapAPIData, None, None]:
        yield OpenWeatherMapAPIData(
            tz_name=self.tzname,
            current=self._current_weather_datamodel(),
            hourly_forecast=[self._hourly_forecast_of(source=item) for item in self.hourly],
            daily_forecast=[self._daily_forecast_of(source=item) for item in self.daily],
            alerts=[_weather_alert_datamodel(source=item) for item in self._alerts]
        )

    def _current_weather_datamodel(self):
        return WeatherForecast(
            dt=self.current['dt'],
            sunrise=self.current['sunrise'],
            sunset=self.current['sunset'],
            temp=self.current.get('temp'),
            pressure=self.current.get('pressure'),
            humidity=self.current.get('humidity'),
            wind_speed=self.current.get('wind_speed'),
            wind_deg=self.current.get('wind_deg'),
            weather=_weather_of(source=self.current),
            rain=self.recursive_search(source=self.current, keywords=['rain', '1h']),
            snow=self.recursive_search(source=self.current, keywords=['snow', '1h'])
        )

    def _hourly_forecast_of(self, source: Dict[str, Any]) -> WeatherForecast:
        return WeatherForecast(
            dt=source['dt'],
            temp=source.get('temp'),
            pressure=source.get('pressure'),
            humidity=source.get('humidity'),
            wind_speed=source.get('wind_speed'),
            wind_deg=source.get('wind_deg'),
            weather=_weather_of(source=source),
            rain=self.recursive_search(source=source, keywords=['rain', '1h']),
            snow=self.recursive_search(source=source, keywords=['snow', '1h']),
            pop=source.get('pop')
        )

    def _daily_forecast_of(self, source: Dict[str, Any]) -> WeatherForecast:
        return WeatherForecast(
            dt=source['dt'],
            temp=self.recursive_search(source=source, keywords=['temp', 'day']),
            temp_min=self.recursive_search(source=source, keywords=['temp', 'min']),
            temp_max=self.recursive_search(source=source, keywords=['temp', 'max']),
            pressure=source.get('pressure'),
            humidity=source.get('humidity'),
            wind_speed=source.get('wind_speed'),
            wind_deg=source.get('wind_deg'),
            weather=_weather_of(source=source),
            rain=source.get('rain'),
            snow=source.get('snow'),
            pop=source.get('pop')
        )

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
