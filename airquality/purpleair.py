######################################################
#
# Author: Davide Colombo
# Date: 19/12/21 11:39
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
SENSOR_COLS = ['sensor_type', 'sensor_name']
APIPARAM_COLS = ['sensor_id', 'ch_key', 'ch_id', 'ch_name', 'last_acquisition']
GEOLOCATION_COLS = ['sensor_id', 'valid_from', 'geom']
SQL_DATETIME_FMT = "%Y-%m-%d %H:%M:%S"


from itertools import count
from datetime import datetime
from airquality.dbadapterabc import DBAdapterABC
from airquality.response import PurpleairResponse
from airquality.sqltable import SQLTable, FilterSQLTable
from airquality.sqldict import MutableSQLDict


def purpleair(dbadapter: DBAdapterABC, url_template: str):

    sensor_table = FilterSQLTable(table_name="sensor", pkey="id", selected_cols=SENSOR_COLS, filter_col="sensor_type", filter_val="purpleair")
    mutable_sensor_dict = MutableSQLDict(table=sensor_table, dbadapter=dbadapter)

    apiparam_table = SQLTable(table_name="api_param", pkey="id", selected_cols=APIPARAM_COLS)
    mutable_apiparam_dict = MutableSQLDict(table=apiparam_table, dbadapter=dbadapter)

    geolocation_table = SQLTable(table_name="sensor_at_location", pkey="id", selected_cols=GEOLOCATION_COLS)
    mutable_geolocation_dict = MutableSQLDict(table=geolocation_table, dbadapter=dbadapter)

    sensor_counter = count(mutable_sensor_dict.start_id)
    apiparam_counter = count(mutable_apiparam_dict.start_id)
    geolocation_counter = count(mutable_geolocation_dict.start_id)

    print(f"\ninsert sensor into: {mutable_sensor_dict!r}")
    print(f"\ninsert sensor API parameters into: {mutable_apiparam_dict!r}")
    print(f"\ninsert sensor locations into: {mutable_geolocation_dict!r}")

    existing_names = []
    for pkey, record in mutable_sensor_dict.items():
        print(f"found sensor indexed by {pkey}: {record!r}")
        existing_names.append(record[1])

    responses = PurpleairResponse(url=url_template, existing_names=existing_names)
    for resp in responses:
        print(f"found new response: {resp!r}")

        sensor_id = next(sensor_counter)
        mutable_sensor_dict[sensor_id] = f"'{resp.type}', '{resp.name}'"

        for chp in resp.channel_properties:
            mutable_apiparam_dict[next(apiparam_counter)] = \
                f"{sensor_id}, '{chp.key}', '{chp.ident}', '{chp.name}', '{resp.created_at}'"

        now = datetime.now().strftime(SQL_DATETIME_FMT)
        mutable_geolocation_dict[next(geolocation_counter)] = f"{sensor_id}, '{now}', NULL, {resp.located_at}"
