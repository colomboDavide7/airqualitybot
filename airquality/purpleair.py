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
from airquality.dbadapter import DBAdapter
from airquality.response import PurpleairResponses
from airquality.sqltable import SQLTable, FilterSQLTable
from airquality.sqldict import MutableSQLDict, FrozenSQLDict


def purpleair(dbadapter: DBAdapter, url_template: str):

    sensor_table = FilterSQLTable(
        dbadapter=dbadapter,
        table_name="sensor", pkey="id",
        selected_cols=SENSOR_COLS,
        filter_col="sensor_type",
        filter_val="purpleair"
    )
    frozen_sensor_dict = FrozenSQLDict(table=sensor_table)
    mutable_sensor_dict = MutableSQLDict(sqldict=frozen_sensor_dict)

    apiparam_table = SQLTable(dbadapter=dbadapter, table_name="api_param", pkey="id", selected_cols=APIPARAM_COLS)
    frozen_apiparam_dict = FrozenSQLDict(table=apiparam_table)
    mutable_apiparam_dict = MutableSQLDict(sqldict=frozen_apiparam_dict)

    geolocation_table = SQLTable(dbadapter=dbadapter, table_name="sensor_at_location", pkey="id", selected_cols=GEOLOCATION_COLS)
    frozen_geolocation_dict = FrozenSQLDict(table=geolocation_table)
    mutable_geolocation_dict = MutableSQLDict(sqldict=frozen_geolocation_dict)

    sensor_counter = count(mutable_sensor_dict.start_id)
    apiparam_counter = count(mutable_apiparam_dict.start_id)
    geolocation_counter = count(mutable_geolocation_dict.start_id)

    existing_names = []
    for pkey, record in mutable_sensor_dict.items():
        print(f"found sensor indexed by {pkey}: {record!r}")
        existing_names.append(record[1])

    responses = PurpleairResponses(url=url_template, existing_names=existing_names)
    for resp in responses:
        print(f"found new response: {resp!r}")

        sensor_id = next(sensor_counter)
        mutable_sensor_dict[sensor_id] = f"'{resp.type}', '{resp.name}'"

        for chp in resp.channel_properties:
            mutable_apiparam_dict[next(apiparam_counter)] = \
                f"{sensor_id}, '{chp.key}', '{chp.ident}', '{chp.name}', '{resp.created_at}'"

        now = datetime.now().strftime(SQL_DATETIME_FMT)
        mutable_geolocation_dict[next(geolocation_counter)] = f"{sensor_id}, '{now}', NULL, {resp.located_at}"
