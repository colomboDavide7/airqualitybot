######################################################
#
# Author: Davide Colombo
# Date: 19/12/21 14:57
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
# TODO: move to environment file
url_template = "https://api.thingspeak.com/channels/{api_id}/feeds.{api_fmt}?api_key={api_key}"

SQL_DATETIME_FMT = "%Y-%m-%d %H:%M:%S"
SENSOR_COLS = ['sensor_type', 'sensor_name']
APIPARAM_COLS = ['sensor_id', 'ch_key', 'ch_id', 'ch_name', 'last_acquisition']
MEASURE_PARAM_COLS = ['param_code', 'param_name', 'param_unit']
STATION_MEASURE_COLS = ['param_id', 'sensor_id', 'param_value', 'timestamp']

MAPPING_1A = {'field1': 'pm1.0_atm_a', 'field2': 'pm2.5_atm_a', 'field3': 'pm10.0_atm_a', 'field6': 'temperature_a',
              'field7': 'humidity_a'}
MAPPING_1B = {'field1': 'pm1.0_atm_b', 'field2': 'pm2.5_atm_b', 'field3': 'pm10.0_atm_b', 'field6': 'pressure_b'}
MAPPING_2A = {'field1': '0.3_um_count_a', 'field2': '0.5_um_count_a', 'field3': '1.0_um_count_a',
              'field4': '2.5_um_count_a', 'field5': '5.0_um_count_a', 'field6': '10.0_um_count_a'}
MAPPING_2B = {'field1': '0.3_um_count_b', 'field2': '0.5_um_count_b', 'field3': '1.0_um_count_b',
              'field4': '2.5_um_count_b', 'field5': '5.0_um_count_b', 'field6': '10.0_um_count_b'}
THINGSPEAK_FIELDS = {'1A': MAPPING_1A, '1B': MAPPING_1B, '2A': MAPPING_2A, '2B': MAPPING_2B}

from itertools import count
from datetime import datetime, timedelta
from airquality.response import ThingspeakResponses
from airquality.sqltable import FilterSQLTable, JoinSQLTable, SQLTable
from airquality.sqldict import FrozenSQLDict, MutableSQLDict, HeavyweightMutableSQLDict


def wrap_value(value: str, default="NULL") -> str:
    return f"'{value}'" if value is not None else default


def add_days(timestamp: datetime, days: int) -> datetime:
    return timestamp + timedelta(days=days)


def thingspeak():
    connection_string = "dbname=airquality host=localhost port=5432 user=root password=a1R-d3B-R00t!"

    station_measure_table = SQLTable(dbconn=connection_string, table_name="station_measurement", pkey="id",
                                     selected_cols=STATION_MEASURE_COLS)
    frozen_mobile_dict = FrozenSQLDict(table=station_measure_table)
    heavyweight_station_dict = HeavyweightMutableSQLDict(sqldict=frozen_mobile_dict)

    thingspeak_measure_param_table = FilterSQLTable(
        dbconn=connection_string,
        table_name="measure_param",
        pkey="id",
        selected_cols=MEASURE_PARAM_COLS,
        filter_col="param_name",
        filter_val="thingspeak"
    )

    frozen_measure_param_dict = FrozenSQLDict(table=thingspeak_measure_param_table)

    thingspeak_sensor_table = FilterSQLTable(
        dbconn=connection_string,
        table_name="sensor",
        pkey="id",
        selected_cols=SENSOR_COLS,
        filter_col="sensor_type",
        filter_val="thingspeak",
        alias="s"
    )

    thingspeak_apiparam_table = JoinSQLTable(
        dbconn=connection_string,
        table_name="api_param",
        pkey="id",
        fkey="sensor_id",
        selected_cols=APIPARAM_COLS,
        alias="a",
        join_table=thingspeak_sensor_table
    )

    frozen_apiparam_dict = FrozenSQLDict(table=thingspeak_apiparam_table)
    mutable_apiparam_dict = MutableSQLDict(sqldict=frozen_apiparam_dict)

    param_code_id = {}
    for key, value in frozen_measure_param_dict.items():
        code, name, unit = value
        print(f"found param with id={key}, code={code}, name={name}, unit={unit}")
        param_code_id[code] = key

    counter = count(heavyweight_station_dict.start_id)
    for pkey, record in mutable_apiparam_dict.items():
        sensor_id, api_key, api_id, ch_name, last_activity = record
        print(f"found Thingspeak sensor with id={sensor_id}: {record!r}")

        field_map = THINGSPEAK_FIELDS[ch_name]
        url = url_template.format(api_key=api_key, api_id=api_id, api_fmt="json") + "&start={start}&end={end}"

        now = datetime.now()
        begin = last_activity + timedelta(0)
        while begin <= now:
            start_date = begin.strftime(SQL_DATETIME_FMT).replace(" ", "%20")
            end_date = add_days(begin, days=7).strftime(SQL_DATETIME_FMT).replace(" ", "%20")
            url_with_date = url.format(start=start_date, end=end_date)
            print(f"looking at time range [{start_date!s} - {end_date!s}]")

            responses = ThingspeakResponses(url=url_with_date, filter_ts=last_activity, field_map=field_map)
            for resp in responses:
                # print(f"found new response: {resp!r}")
                for code, value in resp.values:
                    record_id = next(counter)
                    param_id = param_code_id[code]
                    heavyweight_station_dict[record_id] = f"{param_id}, '{sensor_id}', {wrap_value(value)}, '{resp.created_at}'"

            if responses:
                # Commit all the measurement to insert
                heavyweight_station_dict.commit()

                # Update last acquisition timestamp to avoid redundancy
                last_acquisition = responses[-1].created_at
                mutable_apiparam_dict[pkey] = f"{sensor_id}, '{api_key}', '{api_id}', '{ch_name}', '{last_acquisition}'"

            begin = add_days(begin, days=7)
