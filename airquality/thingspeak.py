######################################################
#
# Author: Davide Colombo
# Date: 19/12/21 14:57
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
MAPPING_1A = {'field1': 'pm1.0_atm_a', 'field2': 'pm2.5_atm_a', 'field3': 'pm10.0_atm_a', 'field6': 'temperature_a',
              'field7': 'humidity_a'}
MAPPING_1B = {'field1': 'pm1.0_atm_b', 'field2': 'pm2.5_atm_b', 'field3': 'pm10.0_atm_b', 'field6': 'pressure_b'}
MAPPING_2A = {'field1': '0.3_um_count_a', 'field2': '0.5_um_count_a', 'field3': '1.0_um_count_a',
              'field4': '2.5_um_count_a', 'field5': '5.0_um_count_a', 'field6': '10.0_um_count_a'}
MAPPING_2B = {'field1': '0.3_um_count_b', 'field2': '0.5_um_count_b', 'field3': '1.0_um_count_b',
              'field4': '2.5_um_count_b', 'field5': '5.0_um_count_b', 'field6': '10.0_um_count_b'}
THINGSPEAK_FIELDS = {'1A': MAPPING_1A, '1B': MAPPING_1B, '2A': MAPPING_2A, '2B': MAPPING_2B}

from itertools import count
from contextlib import suppress
from airquality.dblookup import MeasureParamLookup
from airquality.response import ThingspeakResponse
from airquality.iterableurl import ThingspeakIterableURL
from airquality.sqldict import FrozenSQLDict, MutableSQLDict, HeavyweightInsertSQLDict


def wrap_value(value: str, default="NULL") -> str:
    return f"'{value}'" if value is not None else default


def thingspeak(
        measure_dict: HeavyweightInsertSQLDict,
        measure_param_dict: FrozenSQLDict,
        apiparam_dict: MutableSQLDict,
        url_template: str
):
    measure_counter = count(measure_dict.start_measure_id)
    packet_counter = count(measure_dict.start_packet_id)
    code2id = {MeasureParamLookup(*record).param_code: pkey for pkey, record in measure_param_dict.items()}

    for pkey, record in apiparam_dict.items():
        sensor_id, api_key, api_id, ch_name, last_activity = record
        print(f"found Thingspeak sensor: {record!r}")

        field_map = THINGSPEAK_FIELDS[ch_name]
        url = url_template.format(api_key=api_key, api_id=api_id, api_fmt="json")

        iterable_url = ThingspeakIterableURL(url_template=url, begin=last_activity, step_in_days=7)
        for url in iterable_url:
            items = ThingspeakResponse(url=url, filter_ts=last_activity, field_map=field_map)

            values = ""
            for item in items:
                packet_id = next(packet_counter)
                for code, val in item.values():
                    values += f"({next(measure_counter)}, {packet_id}, {sensor_id}, {code2id[code]}, {wrap_value(val)}, '{item.measured_at()}'),"

            with suppress(ValueError):
                print(f"{values[0:200]} ...... {values[-200:-1]}")
                measure_dict.commit(values.strip(','))

                last_acquisition = items.last_item.measured_at()
                apiparam_dict[pkey] = f"{sensor_id}, '{api_key}', '{api_id}', '{ch_name}', '{last_acquisition}'"
                print(f"last_acquisition: {last_acquisition}")
