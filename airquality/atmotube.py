######################################################
#
# Author: Davide Colombo
# Date: 18/12/21 18:10
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
# TODO: load from the environment file
atmotube_url = "https://api.atmotube.com/api/v1/data?api_key={api_key}&mac={api_id}&order=asc&format=json"

DATE_FMT = "%Y-%m-%d"
SENSOR_COLS = ['sensor_type', 'sensor_name']
APIPARAM_COLS = ['sensor_id', 'ch_key', 'ch_id', 'ch_name', 'last_acquisition']
MEASURE_PARAM_COLS = ['param_code', 'param_name', 'param_unit']
MOBILE_MEASURE_COLS = ['param_id', 'param_value', 'timestamp', 'geom']


from itertools import count
from datetime import datetime, timedelta
from airquality.response import AtmotubeResponses
from airquality.sqltable import FilterSQLTable, JoinSQLTable, SQLTable
from airquality.sqldict import FrozenSQLDict, MutableSQLDict, HeavyweightMutableSQLDict


def wrap_value(value: str, default="NULL") -> str:
    return f"'{value}'" if value is not None else default


def extract_date(timestamp: datetime, fmt=DATE_FMT) -> str:
    return timestamp.date().strftime(fmt)


def add_days(timestamp: datetime, days: int) -> datetime:
    return timestamp + timedelta(days=days)


def atmotube():
    # TODO: read from environment
    connection_string = "dbname=airquality host=localhost port=5432 user=root password=a1R-d3B-R00t!"

    mobile_measure_table = SQLTable(dbconn=connection_string, table_name="mobile_measurement", pkey="id", selected_cols=MOBILE_MEASURE_COLS)
    frozen_mobile_dict = FrozenSQLDict(table=mobile_measure_table)
    heavyweight_mobile_dict = HeavyweightMutableSQLDict(sqldict=frozen_mobile_dict)

    atmotube_measure_param_table = FilterSQLTable(
            dbconn=connection_string,
            table_name="measure_param",
            pkey="id",
            selected_cols=MEASURE_PARAM_COLS,
            filter_col="param_name",
            filter_val="atmotube"
    )

    frozen_measure_param_dict = FrozenSQLDict(table=atmotube_measure_param_table)

    atmotube_sensor_table = FilterSQLTable(
        dbconn=connection_string,
        table_name="sensor",
        pkey="id",
        selected_cols=SENSOR_COLS,
        filter_col="sensor_type",
        filter_val="atmotube",
        alias="s")

    atmotube_apiparam_table = JoinSQLTable(
            dbconn=connection_string,
            table_name="api_param",
            pkey="id",
            fkey="sensor_id",
            selected_cols=APIPARAM_COLS,
            alias="a",
            join_table=atmotube_sensor_table
    )

    frozen_apiparam_dict = FrozenSQLDict(table=atmotube_apiparam_table)
    mutable_apiparam_dict = MutableSQLDict(sqldict=frozen_apiparam_dict)

    param_code_id = {}
    for key, value in frozen_measure_param_dict.items():
        code, name, unit = value
        print(f"found param with id={key}, code={code}, name={name}, unit={unit}")
        param_code_id[code] = key

    counter = count(heavyweight_mobile_dict.start_id)
    for pkey, record in mutable_apiparam_dict.items():
        sensor_id, api_key, api_id, ch_name, last_activity = record
        print(f"found Atmotube sensor with id={sensor_id}: {record!r}")

        url = atmotube_url.format(api_key=api_key, api_id=api_id) + "&date={date}"

        now = datetime.now()
        begin = last_activity + timedelta(0)
        while begin <= now:
            date_to_lookat = extract_date(timestamp=begin, fmt=DATE_FMT)
            url_with_date = url.format(date=date_to_lookat)
            responses = AtmotubeResponses(url=url_with_date, filter_ts=last_activity)
            for resp in responses:
                print(f"found new response at {resp.measured_at}: values={resp.values!r}, coords={resp.coords}")
                for code, val in resp.values:
                    record_id = next(counter)
                    param_id = param_code_id[code]
                    heavyweight_mobile_dict[record_id] = f"{param_id}, {wrap_value(val)}, '{resp.measured_at}', {resp.coords}"

            if responses:
                # commit all the measurements at once
                heavyweight_mobile_dict.commit()

                # Update last activity field at the acquisition time of the last measure stored
                last_acquisition = responses[-1].measured_at
                mutable_apiparam_dict[pkey] = f"{sensor_id}, '{api_key}', '{api_id}', '{ch_name}', '{last_acquisition}'"

            begin = add_days(begin, days=1)
