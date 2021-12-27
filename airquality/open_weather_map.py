######################################################
#
# Author: Davide Colombo
# Date: 23/12/21 19:39
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.dblookup import MeasureParamLookup
from airquality.sqldict import MutableSQLDict, FrozenSQLDict


def openweathermap(service_apiparam: MutableSQLDict, geoarea_dict: FrozenSQLDict, measure_param_dict: FrozenSQLDict, url_template: str):

    measure_param_map = {pid: MeasureParamLookup(*row) for pid, row in measure_param_dict.items()}
    current_weather_param = {m.param_code: pid for pid, m in measure_param_map.items() if m.param_code.startswith("current")}
    hourly_weather_param = {m.param_code: pid for pid, m in measure_param_map.items() if m.param_code.startswith("hourly")}
    daily_weather_param = {m.param_code: pid for pid, m in measure_param_map.items() if m.param_code.startswith("daily")}

    for param_id, param_row in service_apiparam.items():
        api_key, n_requests = param_row
        print(f"found OpenWeatherMap API param at {param_id}: api_key={api_key}, number_of_requests={n_requests}")

        counter = 0
        for geo_id, geo_row in geoarea_dict.items():
            counter += 1
            latitude, longitude = geo_row
            url = url_template.format(lat=latitude, lon=longitude, api_key= api_key)
            print(f"{counter}: {url}")

# print(repr(current_weather_param))
# print(repr(hourly_weather_param))
# print(repr(daily_weather_param))

# for pkey, row in measure_param_dict.items():
#     lookup = MeasureParamLookup(*row)
#     print(f"found measure param at {pkey}: {lookup!r}")
