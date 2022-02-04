######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 15:01
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from typing import Set, Dict, List
from airquality.database.adapter import DatabaseAdapter
from airquality.datamodel.fromdb import GeoareaLocationDM, OpenweathermapKeyDM, \
    SensorInfoDM, SensorLocationDM, SensorApiParamDM


class DatabaseGateway(object):
    def __init__(self, database_adapt: DatabaseAdapter):
        self._database_adapt = database_adapt

    def execute(self, query: str):
        self._database_adapt.execute(query)

# =========== SELECT ID QUERIES
    def _safe_fetch_id(self, query: str):
        row = self._database_adapt.fetchone(query)
        return 1 if row[0] is None else row[0] + 1

    def query_max_sensor_id_plus_one(self) -> int:
        return self._safe_fetch_id(
            query="SELECT MAX(id) FROM level0_raw.sensor;"
        )

    def query_max_mobile_packet_id_plus_one(self) -> int:
        return self._safe_fetch_id(
            query="SELECT MAX(packet_id) FROM level0_raw.mobile_measurement;"
        )

    def query_max_station_packet_id_plus_one(self) -> int:
        return self._safe_fetch_id(
            query="SELECT MAX(packet_id) FROM level0_raw.station_measurement;"
        )

# =========== SELECT SET QUERIES
    def query_poscodes_of_country(self, country_code: str) -> Set[str]:
        rows = self._database_adapt.fetchall(
            query=f"SELECT postal_code FROM level0_raw.geographical_area WHERE country_code = '{country_code}';"
        )
        return {row[0] for row in rows}

    def query_sensor_names_of_type(self, sensor_type: str) -> Set[str]:
        rows = self._database_adapt.fetchall(
            query=f"SELECT sensor_name FROM level0_raw.sensor WHERE sensor_type ILIKE '%{sensor_type}%';"
        )
        return {row[0] for row in rows}

# =========== SELECT MAPPING QUERIES
    def query_measure_param_owned_by(self, owner: str) -> Dict[str, int]:
        query = f"SELECT id, param_code FROM level0_raw.measure_param WHERE param_owner ILIKE '%{owner}%';"
        rows = self._database_adapt.fetchall(query=query)
        if len(rows) == 0:
            raise ValueError(f"Table 'level0_raw.measure_param' doesn't contain sensors owned by = '{owner}'")
        return {code: ident for ident, code in rows}

# =========== SELECT LIST QUERIES
    def query_sensor_apiparam_of_type(self, sensor_type: str) -> List[SensorApiParamDM]:
        query = "SELECT a.sensor_id, a.ch_key, a.ch_id, a.ch_name, a.last_acquisition " \
                "FROM level0_raw.sensor_api_param AS a INNER JOIN level0_raw.sensor AS s " \
                f"ON s.id = a.sensor_id WHERE s.sensor_type ILIKE '%{sensor_type}%';"
        rows = self._database_adapt.fetchall(query=query)
        if len(rows) == 0:
            raise ValueError(f"Table 'level0_raw.sensor_api_param' doesn't contain sensors of type = '{sensor_type}'")
        return [SensorApiParamDM(sid=sid, key=key, id=ident, ch=name, last=last) for sid, key, ident, name, last in rows]

    def query_openweathermap_keys(self) -> List[OpenweathermapKeyDM]:
        query = "SELECT key_value, done_req_min, max_req_min FROM level0_raw.openweathermap_key;"
        rows = self._database_adapt.fetchall(query=query)
        if len(rows) == 0:
            raise ValueError(f"Table 'level0_raw.openweathermap_key' is empty.")
        return [OpenweathermapKeyDM(key=key_val, n_done=done_r, n_max=max_r) for key_val, done_r, max_r in rows]

    def query_weather_conditions(self) -> Dict[str, int]:
        query = "SELECT id, code, icon FROM level0_raw.weather_condition;"
        rows = self._database_adapt.fetchall(query=query)
        if len(rows) == 0:
            raise ValueError(f"Table 'level0_raw.weather_condition' is empty.")
        return {f"{code}_{icon}": id_ for id_, code, icon in rows}

# =========== SELECT SINGLE ROW QUERIES
    def query_last_acquisition_of(self, sensor_id: int, ch_name: str) -> datetime:
        query = "SELECT last_acquisition FROM level0_raw.sensor_api_param " \
                f"WHERE sensor_id = {sensor_id} AND ch_name = '{ch_name}';"
        row = self._database_adapt.fetchone(query=query)
        if row is None:
            raise ValueError(f"Cannot found records corresponding to sensor_id = '{sensor_id}' and "
                             f"channel_name = '{ch_name}' in 'level0_raw.sensor_api_param' table.")
        return row[0]

    def query_place_location(self, country_code: str, place_name: str) -> GeoareaLocationDM:
        query = "SELECT id, ST_X(geom), ST_Y(geom) FROM level0_raw.geographical_area " \
                f"WHERE country_code = '{country_code}' AND place_name = '{place_name}';"
        row = self._database_adapt.fetchone(query=query)
        if row is None:
            raise ValueError(f"Cannot found a record corresponding to country_code = '{country_code}' and "
                             f"place_name = '{place_name}' in 'level0_raw.geographical_area' table")
        return GeoareaLocationDM(id=row[0], longitude=row[1], latitude=row[2])

    def query_fixed_sensor_unique_info(self, sensor_id: int):
        query = "SELECT s.id, s.sensor_name, ST_X(l.geom), ST_Y(l.geom) FROM level0_raw.sensor AS s " \
                "INNER JOIN level0_raw.sensor_at_location AS l ON s.id = l.sensor_id " \
                f"WHERE l.sensor_id = {sensor_id} ORDER BY l.valid_from DESC;"
        row = self._database_adapt.fetchone(query=query)
        if row is None:
            raise ValueError(f"Cannot found record corresponding to sensor_id = "
                             f"'{sensor_id}' in 'level0_raw.sensor_at_location' table")
        return SensorInfoDM(sensor_id=row[0], sensor_name=row[1], sensor_lng=row[2], sensor_lat=row[3])

    def query_mobile_sensor_unique_info(self, sensor_id: int):
        query = f"SELECT id, sensor_name FROM level0_raw.sensor WHERE id = {sensor_id};"
        row = self._database_adapt.fetchone(query=query)
        if row is None:
            raise ValueError(f"Cannot found record corresponding to sensor_id = "
                             f"'{sensor_id}' in 'level0_raw.sensor' table.")
        return SensorInfoDM(sensor_id=row[0], sensor_name=row[1])

    def query_purpleair_sensor_location(self, sensor_index: int) -> SensorLocationDM:
        query = "SELECT l.sensor_id, ST_X(geom), ST_Y(geom) FROM level0_raw.sensor_at_location AS l INNER JOIN " \
                "level0_raw.sensor AS s ON s.id = l.sensor_id WHERE s.sensor_type ILIKE '%purpleair%' AND " \
                f"sensor_name ILIKE '%{sensor_index}%' AND valid_to IS NULL;"
        row = self._database_adapt.fetchone(query=query)
        if row is None:
            raise ValueError(f"Cannot found a record corresponding to sensor_type = 'purpleair' which name"
                             f"contains sensor_index = '{sensor_index}' in 'level0_raw.sensor' table.")
        return SensorLocationDM(sensor_id=row[0], longitude=row[1], latitude=row[2])

    def query_hourly_forecast_records(self) -> Set:
        return set(
            self._database_adapt.fetchall(query="SELECT * FROM level0_raw.hourly_forecast;")
        )

    def query_daily_forecast_records(self) -> Set:
        return set(
            self._database_adapt.fetchall(query="SELECT * FROM level0_raw.daily_forecast;")
        )

    def exists_weather_alert_of(self, alert, geoarea_id: int) -> bool:
        row = self._database_adapt.fetchone(
            query=f"SELECT id FROM level0_raw.weather_alert WHERE geoarea_id = {geoarea_id} "
                  f"AND alert_event = '{alert.event}' AND alert_begin = '{alert.begin}';"
        )
        return False if row is None else True
