######################################################
#
# Author: Davide Colombo
# Date: 19/12/21 11:39
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
SQL_DATETIME_FMT = "%Y-%m-%d %H:%M:%S"


from itertools import count
from datetime import datetime
from airquality.dblookup import SensorLookup
from airquality.response import PurpleairResponse
from airquality.sqldict import MutableSQLDict


def purpleair(
        sensor_dict: MutableSQLDict,
        apiparam_dict: MutableSQLDict,
        geolocation_dict: MutableSQLDict,
        url_template: str
):
    sensor_counter = count(sensor_dict.start_id)
    apiparam_counter = count(apiparam_dict.start_id)
    geolocation_counter = count(geolocation_dict.start_id)

    existing_names = {SensorLookup(*record).sensor_name for record in sensor_dict.values()}
    responses = PurpleairResponse(url=url_template, existing_names=existing_names)

    for resp in responses:
        sensor_id = next(sensor_counter)
        sensor_dict[sensor_id] = f"'{resp.type()}', '{resp.name()}'"

        for chp in resp.channel_properties():
            apiparam_dict[next(apiparam_counter)] = \
                f"{sensor_id}, '{chp.key}', '{chp.ident}', '{chp.name}', '{resp.created_at()}'"

        now = datetime.now().strftime(SQL_DATETIME_FMT)
        geolocation_dict[next(geolocation_counter)] = f"{sensor_id}, '{now}', NULL, {resp.located_at()}"
