######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 15:01
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from typing import Set, Dict, List
from airquality.datamodel.apiparam import APIParam
from airquality.datamodel.apidata import CityOfGeoarea
from airquality.database.adapter import DatabaseAdapter
from airquality.datamodel.geolocation import Geolocation
from airquality.datamodel.sensor_ident import SensorIdentity
from airquality.datamodel.openweathermap_key import OpenweathermapKey
from airquality.extra.decorators import throw_on, constructor_of, get_at, dict_from_tuples


class DatabaseGateway(object):
    def __init__(self, database_adapt: DatabaseAdapter):
        self._database_adapt = database_adapt

    def execute(self, query: str):
        print(query)
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
    @dict_from_tuples(key_index=1)
    @throw_on(sentinel_value=[], exc_type=ValueError)
    def query_measure_param_owned_by(self, owner: str) -> Dict[str, int]:
        return self._database_adapt.fetchall(
            query=f"SELECT id, param_code FROM level0_raw.measure_param WHERE param_owner ILIKE '%{owner}%';"
        )

# =========== SELECT LIST QUERIES
    @throw_on(sentinel_value=[], exc_type=ValueError)
    def query_sensor_apiparam_of_type(self, sensor_type: str) -> List[APIParam]:
        rows = self._database_adapt.fetchall(
            query="SELECT a.sensor_id, a.ch_key, a.ch_id, a.ch_name, a.last_acquisition "
                  "FROM level0_raw.sensor_api_param AS a INNER JOIN level0_raw.sensor AS s "
                  f"ON s.id = a.sensor_id WHERE s.sensor_type ILIKE '%{sensor_type}%';"
        )
        return [APIParam(sensor_id=sid,
                         api_key=key,
                         api_id=ident,
                         ch_name=name,
                         last_acquisition=last) for sid, key, ident, name, last in rows]

    @throw_on(sentinel_value=[], exc_type=ValueError)
    def query_openweathermap_keys(self) -> List[OpenweathermapKey]:
        rows = self._database_adapt.fetchall(
            query="SELECT key_value, done_req_min, max_req_min FROM level0_raw.openweathermap_key;"
        )
        return [OpenweathermapKey(key_value=key_val,
                                  done_requests_per_minute=done_r,
                                  max_requests_per_minute=max_r) for key_val, done_r, max_r in rows]

    @throw_on(sentinel_value=[], exc_type=ValueError)
    def query_weather_conditions(self):
        return self._database_adapt.fetchall(
            query="SELECT id, code, icon FROM level0_raw.weather_condition;"
        )

# =========== SELECT SINGLE ROW QUERIES
    @get_at(index=0)
    @throw_on(sentinel_value=None, exc_type=ValueError)
    def query_last_acquisition_of(self, sensor_id: int, ch_name: str) -> datetime:
        return self._database_adapt.fetchone(
            query="SELECT last_acquisition "
                  "FROM level0_raw.sensor_api_param "
                  f"WHERE sensor_id = {sensor_id} AND ch_name = '{ch_name}';"
        )

    @constructor_of(obj_type=CityOfGeoarea)
    @throw_on(sentinel_value=None, exc_type=ValueError)
    def query_geolocation_of(self, country_code: str, place_name: str):
        return self._database_adapt.fetchone(
            query="SELECT id, ST_X(geom), ST_Y(geom) "
                  "FROM level0_raw.geographical_area "
                  f"WHERE country_code = '{country_code}' AND place_name = '{place_name}';"
        )

    @constructor_of(obj_type=SensorIdentity)
    @throw_on(sentinel_value=None, exc_type=ValueError)
    def query_fixed_sensor_unique_info(self, sensor_id: int):
        return self._database_adapt.fetchone(
            query="SELECT s.id, s.sensor_name, ST_X(l.geom), ST_Y(l.geom) FROM level0_raw.sensor AS s "
                  "INNER JOIN level0_raw.sensor_at_location AS l ON s.id = l.sensor_id "
                  f"WHERE l.sensor_id = {sensor_id} ORDER BY l.valid_from DESC;"
        )

    @constructor_of(obj_type=SensorIdentity)
    @throw_on(sentinel_value=None, exc_type=ValueError)
    def query_mobile_sensor_unique_info(self, sensor_id: int):
        return self._database_adapt.fetchone(
            query=f"SELECT id, sensor_name FROM level0_raw.sensor WHERE id = {sensor_id};"
        )

    @constructor_of(obj_type=Geolocation)
    @throw_on(sentinel_value=None, exc_type=ValueError)
    def query_purpleair_location_of(self, sensor_index: int) -> Geolocation:
        return self._database_adapt.fetchone(
            query="SELECT l.sensor_id, ST_X(geom), ST_Y(geom) FROM level0_raw.sensor_at_location AS l "
                  "INNER JOIN level0_raw.sensor AS s ON s.id = l.sensor_id "
                  f"WHERE s.sensor_type ILIKE '%purpleair%' AND sensor_name ILIKE '%{sensor_index}%' "
                  "AND valid_to IS NULL;"
        )

    def query_hourly_forecast_records(self) -> Set:
        return set(self._database_adapt.fetchall(
            query="SELECT * FROM level0_raw.hourly_forecast;"
        ))

    def query_daily_forecast_records(self) -> Set:
        return set(self._database_adapt.fetchall(
            query="SELECT * FROM level0_raw.daily_forecast;"
        ))

    def __repr__(self):
        return f"self=(type='{type(self).__name__}', id='{id(self)}')"
