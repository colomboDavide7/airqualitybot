######################################################
#
# Author: Davide Colombo
# Date: 18/12/21 18:10
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
DATE_FMT = "%Y-%m-%d"
SENSOR_COLS = ['sensor_type', 'sensor_name']
APIPARAM_COLS = ['sensor_id', 'ch_key', 'ch_id', 'ch_name', 'last_acquisition']
MEASURE_PARAM_COLS = ['param_code', 'param_name', 'param_unit']
MOBILE_MEASURE_COLS = ['param_id', 'param_value', 'timestamp', 'geom']


from itertools import count
from datetime import datetime, timedelta
from airquality.dbadapter import DBAdapterABC
from airquality.response import AtmotubeResponse
from airquality.sqltable import FilterSQLTable, JoinSQLTable, SQLTable
from airquality.sqldict import FrozenSQLDict, MutableSQLDict, HeavyweightMutableSQLDict


def wrap_value(value: str, default="NULL") -> str:
    return f"'{value}'" if value is not None else default


def extract_date(timestamp: datetime, fmt=DATE_FMT) -> str:
    return timestamp.date().strftime(fmt)


def add_days(timestamp: datetime, days: int) -> datetime:
    return timestamp + timedelta(days=days)


def atmotube(
        mobile_dict: HeavyweightMutableSQLDict,
        measure_param_dict: FrozenSQLDict,
        apiparam_dict: MutableSQLDict,
        url_template: str
):
    counter = count(mobile_dict.start_id)

    param_code_id = {record[0]: pkey for pkey, record in measure_param_dict.items()}

    for pkey, record in apiparam_dict.items():
        sensor_id, api_key, api_id, ch_name, last_activity = record
        print(f"found Atmotube sensor with id={sensor_id}: {record!r}")

        url = url_template.format(api_key=api_key, api_id=api_id, api_fmt="json") + "&date={date}"

        now = datetime.now()
        begin = last_activity + timedelta(0)
        while begin <= now:
            date_to_lookat = extract_date(timestamp=begin, fmt=DATE_FMT)
            url_with_date = url.format(date=date_to_lookat)
            items = AtmotubeResponse(url=url_with_date, filter_ts=last_activity)
            for item in items:
                print(f"found new response item: {item!r}")
                for code, val in item.values:
                    record_id = next(counter)
                    param_id = param_code_id[code]
                    mobile_dict[record_id] = f"{param_id}, {wrap_value(val)}, '{item.measured_at}', {item.located_at}"

            if items:
                # commit all the measurements at once
                mobile_dict.commit()

                # Update last activity field at the acquisition time of the last measure stored
                last_resp = items[-1]
                last_acquisition = last_resp.measured_at
                last_activity = last_resp.measured_at_datetime
                apiparam_dict[pkey] = f"{sensor_id}, '{api_key}', '{api_id}', '{ch_name}', '{last_acquisition}'"

            begin = add_days(begin, days=1)
