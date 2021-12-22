######################################################
#
# Author: Davide Colombo
# Date: 18/12/21 18:10
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from itertools import count
from contextlib import suppress
from airquality.response import AtmotubeResponse
from airquality.dblookup import MeasureParamLookup
from airquality.iterableurl import AtmotubeIterableURL
from airquality.sqldict import FrozenSQLDict, MutableSQLDict, HeavyweightInsertSQLDict


def wrap_value(value: str, default="NULL") -> str:
    return f"'{value}'" if value is not None else default


def atmotube(
        mobile_dict: HeavyweightInsertSQLDict,
        measure_param_dict: FrozenSQLDict,
        apiparam_dict: MutableSQLDict,
        url_template: str
):
    measure_counter = count(mobile_dict.start_id)
    code2id = {MeasureParamLookup(*record).param_code: pkey for pkey, record in measure_param_dict.items()}

    for pkey, record in apiparam_dict.items():
        print(f"found API param: {record!r}")
        sensor_id, api_key, api_id, ch_name, last_activity = record

        url = url_template.format(api_key=api_key, api_id=api_id, api_fmt="json")
        iterable_url = AtmotubeIterableURL(url_template=url, begin=last_activity)

        for url in iterable_url:
            items = AtmotubeResponse(url=url, filter_ts=last_activity)

            values = ','.join(
                f"({next(measure_counter)}, {code2id[code]}, {wrap_value(val)}, '{item.measured_at()}', {item.located_at()})"
                for item in items for code, val in item.values()
            )

            with suppress(ValueError):
                print(f"{values[0:200]} ...... {values[-200:-1]}")
                mobile_dict.commit(values)

                last_acquisition = items.last_item.measured_at()
                apiparam_dict[pkey] = f"{sensor_id}, '{api_key}', '{api_id}', '{ch_name}', '{last_acquisition}'"
                print(f"last_acquisition: {last_acquisition}")
