######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 20:12
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Generator, Dict
import airquality.extra.weather as wextra
from airquality.iterables.abc import IterableItemsABC
from airquality.datamodel.fromapi import PurpleairDM, AtmotubeDM, ThingspeakDM, OpenweathermapDM


class PurpleairIterableDatamodels(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and defines the business rules for
    extracting the items from a PurpleAir json response.

    Keyword arguments:
        *json_response*         the json response from PurpleAir API.

    """

    def __init__(self, json_response: Dict):
        self._fields = json_response['fields']
        self._data = json_response['data']

    def items(self) -> Generator[PurpleairDM, None, None]:
        return (PurpleairDM(**(dict(zip(self._fields, data)))) for data in self._data)


class AtmotubeIterableDatamodels(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and defines the business rules for
    extracting the items from an Atmotube json response.

    Keyword arguments:
        *json_response*         the json response from Atmotube API.

    """

    def __init__(self, json_response: Dict):
        self._items = json_response['data']['items']

    def items(self) -> Generator[AtmotubeDM, None, None]:
        return (AtmotubeDM(**item) for item in self._items)


class ThingspeakIterableDatamodels(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and defines the business rules for
    extracting the items from a Thingspeak json response.

    Keyword arguments:
        *json_response*         the json response from Thingspeak API.

    """

    def __init__(self, json_response: Dict):
        self._feeds = json_response['feeds']

    def items(self) -> Generator[ThingspeakDM, None, None]:
        return (ThingspeakDM(**item) for item in self._feeds)


class OpenweathermapIterableDatamodels(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and defines the business rules for
    extracting current weather, hourly forecast and daily forecast items from an OpenWeatherMap response.

    Keyword arguments:
        *json_response*         the json response from OneCallAPI service of OpenWeatherMap.

    """

    def __init__(self, json_response: Dict):
        self.tzname = json_response['timezone']               # the time zone name for the requested location.
        self.current = json_response['current']               # the current weather dict.
        self.hourly = json_response['hourly']                 # the list of hourly weather forecast.
        self.daily = json_response['daily']                   # the list of daily weather forecast.
        self._alerts = json_response.get('alerts', ())        # the list of weather alerts (DEFAULTS TO EMPTY LIST)

    def items(self) -> Generator[OpenweathermapDM, None, None]:
        yield OpenweathermapDM(
            tz_name=self.tzname,
            current=wextra.current_weather_datamodel(source=self.current),
            hourly_forecast=[wextra.hourly_forecast_datamodel(source=item) for item in self.hourly],
            daily_forecast=[wextra.daily_forecast_datamodel(source=item) for item in self.daily],
            alerts=[wextra.weather_alert_of(source=item) for item in self._alerts]
        )
