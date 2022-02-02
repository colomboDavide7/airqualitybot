# ======================================
# @author:  Davide Colombo
# @date:    2022-02-2, mer, 12:20
# ======================================
"""
This module contains a set of facility functions for building weather datamodels.
"""

from typing import Dict, List
from airquality.datamodel.fromapi import WeatherDM, WeatherConditionsDM, WeatherAlertDM


def _nested_search_dict(source: Dict, keywords: List):
    if type(source) != dict:
        return source
    return _nested_search_dict(source=source.get(keywords.pop(0)), keywords=keywords)


def _weather_of(source: Dict) -> List[WeatherDM]:
    weather = source.get('weather')
    return [WeatherDM(**w) for w in weather] if weather is not None else weather


def weather_alert_of(source: Dict) -> WeatherAlertDM:
    return WeatherAlertDM(
        sender_name=source['sender_name'],
        alert_event=source['event'],
        alert_begin=source['start'],
        alert_until=source['end'],
        description=source['description']
    )


def current_weather_of(source: Dict) -> WeatherConditionsDM:
    return WeatherConditionsDM(
        dt=source['dt'],
        sunrise=source['sunrise'],
        sunset=source['sunset'],
        temp=source.get('temp'),
        pressure=source.get('pressure'),
        humidity=source.get('humidity'),
        wind_speed=source.get('wind_speed'),
        wind_deg=source.get('wind_deg'),
        weather=_weather_of(source=source),
        rain=_nested_search_dict(source=source, keywords=['rain', '1h']),
        snow=_nested_search_dict(source=source, keywords=['snow', '1h'])
    )


def hourly_forecast_of(source: Dict) -> WeatherConditionsDM:
    return WeatherConditionsDM(
        dt=source['dt'],
        temp=source.get('temp'),
        pressure=source.get('pressure'),
        humidity=source.get('humidity'),
        wind_speed=source.get('wind_speed'),
        wind_deg=source.get('wind_deg'),
        weather=_weather_of(source=source),
        rain=_nested_search_dict(source=source, keywords=['rain', '1h']),
        snow=_nested_search_dict(source=source, keywords=['snow', '1h']),
        pop=source.get('pop')
    )


def daily_forecast_of(source: Dict) -> WeatherConditionsDM:
    return WeatherConditionsDM(
        dt=source['dt'],
        temp=_nested_search_dict(source=source, keywords=['temp', 'day']),
        temp_min=_nested_search_dict(source=source, keywords=['temp', 'min']),
        temp_max=_nested_search_dict(source=source, keywords=['temp', 'max']),
        pressure=source.get('pressure'),
        humidity=source.get('humidity'),
        wind_speed=source.get('wind_speed'),
        wind_deg=source.get('wind_deg'),
        weather=_weather_of(source=source),
        rain=source.get('rain'),
        snow=source.get('snow'),
        pop=source.get('pop')
    )
