######################################################
#
# Author: Davide Colombo
# Date: 28/12/21 10:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import json
import psycopg2
import itertools
import urllib.request
from typing import Dict, Set
from datetime import datetime, timedelta
from airquality.dblookup import SensorAPIParam

MAPPING_1A = {'field1': 'pm1.0_atm_a', 'field2': 'pm2.5_atm_a', 'field3': 'pm10.0_atm_a', 'field6': 'temperature_a',
              'field7': 'humidity_a'}
MAPPING_1B = {'field1': 'pm1.0_atm_b', 'field2': 'pm2.5_atm_b', 'field3': 'pm10.0_atm_b', 'field6': 'pressure_b'}
MAPPING_2A = {'field1': '0.3_um_count_a', 'field2': '0.5_um_count_a', 'field3': '1.0_um_count_a',
              'field4': '2.5_um_count_a', 'field5': '5.0_um_count_a', 'field6': '10.0_um_count_a'}
MAPPING_2B = {'field1': '0.3_um_count_b', 'field2': '0.5_um_count_b', 'field3': '1.0_um_count_b',
              'field4': '2.5_um_count_b', 'field5': '5.0_um_count_b', 'field6': '10.0_um_count_b'}
THINGSPEAK_FIELDS = {'1A': MAPPING_1A, '1B': MAPPING_1B, '2A': MAPPING_2A, '2B': MAPPING_2B}


class Thingspeak:

    def __init__(self, personality: str, url_template: str, **url_options):
        self.url_template = url_template
        self.url_options = url_options
        self.personality = personality
        self._conn = psycopg2.connect(database=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port)
        self._measure_param = {}
        self._apiparam = set()

    @property
    def dbname(self):
        return os.environ['database']

    @property
    def user(self):
        return os.environ['user']

    @property
    def password(self):
        return os.environ['password']

    @property
    def host(self):
        return os.environ['host']

    @property
    def port(self):
        return os.environ['port']

    @property
    def start_record_id(self) -> int:
        with self._conn.cursor() as cur:
            cur.execute("SELECT MAX(id) FROM level0_raw.station_measurement;")
            self._conn.commit()
            row = cur.fetchone()
            return 1 if row[0] is None else row[0] + 1

    @property
    def start_packet_id(self) -> int:
        with self._conn.cursor() as cur:
            cur.execute("SELECT MAX(packet_id) FROM level0_raw.station_measurement;")
            self._conn.commit()
            row = cur.fetchone()
            return 1 if row[0] is None else row[0] + 1

    @property
    def measure_param(self) -> Dict[str, int]:
        with self._conn.cursor() as cur:
            cur.execute(
                f"SELECT param_code, id FROM level0_raw.measure_param WHERE param_owner ILIKE '%{self.personality}%';")
            self._conn.commit()
            rows = cur.fetchall()
            if not rows:
                raise ValueError(f"{type(self).__name__} expected *measure_param* table to be not empty!")
            return {param_code: param_id for param_code, param_id in rows}

    @property
    def apiparam(self) -> Set[SensorAPIParam]:
        with self._conn.cursor() as cur:
            cur.execute("SELECT a.id, a.sensor_id, a.ch_key, a.ch_id, a.ch_name, a.last_acquisition "
                        "FROM level0_raw.sensor_api_param AS a INNER JOIN level0_raw.sensor AS s ON s.id = a.sensor_id "
                        f"WHERE s.sensor_type ILIKE '%{self.personality}%';")
            self._conn.commit()
            rows = cur.fetchall()
            if not rows:
                raise ValueError(f"{type(self).__name__} expected *sensor_api_param* table to be not empty!")
            return {SensorAPIParam(*row) for row in rows}

    def execute(self, step_in_days=7):
        measure_param = self.measure_param
        apiparam = self.apiparam
        for param in apiparam:
            print(f"found API param: {param!r}")
            field_map = THINGSPEAK_FIELDS[param.ch_name]

            self.url_options.update(**param.database_url_param)
            begin = param.last_acquisition
            until = datetime.now()
            while begin <= until:
                tmp_end = begin + timedelta(days=step_in_days)
                tmp_end = until if tmp_end >= until else tmp_end

                start_ts = begin.strftime("%Y-%m-%d %H:%M:%S").replace(" ", "%20")
                end_ts = tmp_end.strftime("%Y-%m-%d %H:%M:%S").replace(" ", "%20")
                self.url_options.update({"start": start_ts, "end": end_ts})
                url = self.url_template.format(**self.url_options)
                # print(url)

                with urllib.request.urlopen(url) as u:
                    raw = u.read()
                    parsed = json.loads(raw)

                    sql_values = ""
                    record_id = itertools.count(self.start_record_id)
                    packet_id = itertools.count(self.start_packet_id)
                    items = parsed['feeds']
                    for item in items:

                        # Extract the datetime timestamp to check if the item is obsolete or not
                        ts_str = item['created_at']
                        ts_dt = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ")
                        if ts_dt > param.last_acquisition:
                            pid = next(packet_id)
                            timestamp = ts_dt.strftime("%Y-%m-%d %H:%M:%S")
                            for field_number in field_map:
                                param_value = item[field_number]
                                param_code = field_map[field_number]
                                param_id = measure_param[param_code]
                                sql_values += f"({next(record_id)}, {pid}, {param.sensor_id}, {param_id}, '{param_value}', '{timestamp}'),"

                    if items:
                        last_activity = items[-1]['created_at']
                        fmt_last_activity = last_activity.replace("T", " ").strip('Z')

                        print(f"{sql_values[0:200]} ....... {sql_values[-201:-1]}")
                        with self._conn.cursor() as cur:
                            cur.execute(f"INSERT INTO level0_raw.station_measurement VALUES {sql_values.strip(',')};")
                            cur.execute(f"UPDATE level0_raw.sensor_api_param SET last_acquisition = '{fmt_last_activity}' "
                                        f"WHERE sensor_id = {param.sensor_id}")
                            self._conn.commit()

                begin += timedelta(days=step_in_days)
