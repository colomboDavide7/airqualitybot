######################################################
#
# Author: Davide Colombo
# Date: 23/12/21 19:39
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.sqldict import MutableSQLDict, FrozenSQLDict


def openweathermap(service_apiparam: MutableSQLDict, geoarea_dict: FrozenSQLDict, url_template: str):
    print("running OpenWeatherMap....")

    for param_id, param_row in service_apiparam.items():
        api_key, n_requests = param_row
        print(f"found OpenWeatherMap API param at {param_id}: api_key={api_key}, number_of_requests={n_requests}")

        for geo_id, geo_row in geoarea_dict.items():
            latitude, longitude = geo_row
            url = url_template.format(lat=latitude, lon=longitude, api_key= api_key)
            print(url)
