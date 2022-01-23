######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 15:01
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import logging
from datetime import datetime
from typing import Set, Dict, List
import airquality.database as queries
from airquality.datamodel.apiparam import APIParam
from airquality.database.adapter import DatabaseAdapter
from airquality.datamodel.service_param import ServiceParam
from airquality.datamodel.sensor_ident import SensorIdentity
from airquality.datamodel.apidata import WeatherCityData, CityOfGeoarea
from airquality.core.response_builder import \
    AddFixedSensorResponseBuilder, \
    AddMobileMeasureResponseBuilder, \
    AddStationMeasuresResponseBuilder, \
    AddPlacesResponseBuilder, \
    AddOpenWeatherMapDataResponseBuilder


class DatabaseGateway(object):
    """
    A class that defines how the application can interact with the database.

    Every single query that can be executed must be defined here within a method.

    Keyword arguments:
        *database_adapt*            the concrete implementation of DatabaseAdapter interface for executing actions
                                    against the database.

    """

    def __init__(self, database_adapt: DatabaseAdapter):
        self.database_adapt = database_adapt
        self._logger = logging.getLogger(__name__)

    def _raise(self, cause: str):
        self._logger.exception(cause)
        raise ValueError(cause)

    def _fetch_all(self, query: str, err_msg=""):
        rows = self.database_adapt.fetchall(query)
        if not rows and err_msg:
            self._raise(err_msg)
        return rows

    def _fetch_one(self, query: str, err_msg: str):
        row = self.database_adapt.fetchone(query)
        if row is None:
            self._raise(err_msg)
        return row

    def _fetch_id(self, query: str):
        row = self.database_adapt.fetchone(query)
        return 1 if row[0] is None else row[0] + 1

# =========== SELECT ID QUERIES
    def query_max_sensor_id_plus_one(self) -> int:
        return self._fetch_id(
            query=queries.SELECT_MAX_SENS_ID
        )

    def query_max_mobile_packet_id_plus_one(self) -> int:
        return self._fetch_id(
            query=queries.SELECT_MAX_MOBILE_PACK_ID
        )

    def query_max_station_packet_id_plus_one(self) -> int:
        return self._fetch_id(
            query=queries.SELECT_MAX_STATION_PACK_ID
        )

# =========== SELECT SET QUERIES
    def query_poscodes_of_country(self, country_code: str) -> Set[str]:
        rows = self._fetch_all(
            query=queries.SELECT_POSCODES_OF.format(code=country_code)
        )
        return {row[0] for row in rows}

    def query_sensor_names_of_type(self, sensor_type: str) -> Set[str]:
        rows = self._fetch_all(
            query=queries.SELECT_SENSOR_NAMES.format(type=sensor_type)
        )
        return {row[0] for row in rows}

# =========== SELECT MAPPING QUERIES
    def query_measure_param_owned_by(self, owner: str) -> Dict[str, int]:
        rows = self._fetch_all(
            query=queries.SELECT_MEASURE_PARAM.format(owner=owner),
            err_msg=f"database failed to query 'measure_param' owned by '{owner}'"
        )
        return {code: ident for ident, code in rows}

# =========== SELECT LIST QUERIES
    def query_sensor_apiparam_of_type(self, sensor_type: str) -> List[APIParam]:
        rows = self._fetch_all(
            query=queries.SELECT_SENS_API_PARAM_OF.format(type=sensor_type),
            err_msg=f"database failed to query 'sensor_api_param' of type '{sensor_type}'"
        )
        return [
            APIParam(sensor_id=sid, api_key=key, api_id=ident, ch_name=name, last_acquisition=last) for
            sid, key, ident, name, last in rows
        ]

    def query_service_apiparam_of(self, service_name: str) -> List[ServiceParam]:
        rows = self._fetch_all(
            query=queries.SELECT_SERVICE_API_PARAM_OF.format(sn=service_name),
            err_msg=f"database failed to query 'service_api_param' for service '{service_name}'"
        )
        return [ServiceParam(api_key=api_key, n_requests=nreq) for api_key, nreq in rows]

    def query_weather_conditions(self):
        return self._fetch_all(
            query=queries.SELECT_WEATHER_COND,
            err_msg=f"database failed to query 'weather_condition'"
        )

# =========== SELECT SINGLE ROW QUERIES
    def query_last_acquisition_of(self, sensor_id: int, ch_name: str) -> datetime:
        row = self._fetch_one(
            query=queries.SELECT_LAST_ACQUISITION_OF.format(sid=sensor_id, ch=ch_name),
            err_msg=f"database failed to query 'sensor_api_param' at sensor id '{sensor_id}' and channel '{ch_name}'"
        )
        return row[0]

    def query_service_id_from_name(self, service_name: str) -> int:
        row = self._fetch_one(
            query=queries.SELECT_SERVICE_ID_FROM.format(sn=service_name),
            err_msg=f"database failed to query 'service_id' for service '{service_name}'!!!"
        )
        return row[0]

    def query_geolocation_of(self, city: WeatherCityData) -> CityOfGeoarea:
        row = self._fetch_one(
            query=queries.SELECT_GEOLOCATION_OF.format(country=city.country_code, place=city.place_name),
            err_msg=f"database failed to query 'geographical_area' for city {city!r}!!!"
        )
        return CityOfGeoarea(
            geoarea_id=row[0],
            longitude=row[1],
            latitude=row[2]
        )

    def query_fixed_sensor_unique_info(self, sensor_id: int):
        row = self._fetch_one(
            query=queries.SELECT_FIXED_SENSOR_UNIQUE_INFO.format(sid=sensor_id),
            err_msg=f"database failed to query 'sensor' for id = '{sensor_id}'"
        )
        return SensorIdentity(
            sensor_id=row[0],
            sensor_name=row[1],
            sensor_lat=row[2],
            sensor_lng=row[3]
        )

# =========== INSERT QUERIES
    def insert_weather_data(self, responses: AddOpenWeatherMapDataResponseBuilder):
        cval = hval = dval = ""
        for r in responses:
            cval += f"{r.current_weather_record},"
            hval += f"{r.hourly_forecast_record},"
            dval += f"{r.daily_forecast_record},"
        current_weather_query = queries.INSERT_CURRENT_WEATHER_DATA.format(val=cval.strip(','))
        hourly_forecast_query = queries.INSERT_HOURLY_FORECAST_DATA.format(val=hval.strip(','))
        daily_forecast_query = queries.INSERT_DAILY_FORECAST_DATA.format(val=dval.strip(','))
        self.database_adapt.execute(f"{current_weather_query} {hourly_forecast_query} {daily_forecast_query}")

    def insert_sensors(self, responses: AddFixedSensorResponseBuilder):
        sval = pval = gval = ""
        for r in responses:
            sval += f"{r.sensor_record},"
            pval += f"{r.apiparam_record},"
            gval += f"{r.geolocation_record},"
        sensor_query = queries.INSERT_SENSORS.format(val=sval.strip(','))
        apiparam_query = queries.INSERT_SENSOR_API_PARAM.format(val=pval.strip(','))
        geolocation_query = queries.INSERT_SENSOR_LOCATION.format(val=gval.strip(','))
        self.database_adapt.execute(f"{sensor_query} {apiparam_query} {geolocation_query}")

    def insert_mobile_measures(self, responses: AddMobileMeasureResponseBuilder):
        values = ','.join(resp.measure_record for resp in responses)
        measure_query = queries.INSERT_MOBILE_MEASURES.format(val=values)
        self.database_adapt.execute(measure_query)

    def insert_station_measures(self, responses: AddStationMeasuresResponseBuilder):
        values = ','.join(resp.measure_record for resp in responses)
        query = queries.INSERT_STATION_MEASURES.format(val=values)
        self.database_adapt.execute(query)

    def insert_places(self, responses: AddPlacesResponseBuilder):
        values = ','.join(resp.place_record for resp in responses)
        query = queries.INSERT_PLACES.format(val=values)
        self.database_adapt.execute(query)

# =========== UPDATE QUERIES
    def update_last_acquisition_of(self, timestamp: datetime, sensor_id: int, ch_name: str):
        self.database_adapt.execute(
            query=queries.UPDATE_LAST_CH_TIMEST.format(
                time=timestamp,
                sid=sensor_id,
                ch=ch_name
            )
        )

# =========== DELETE QUERIES
    def delete_all_from_hourly_weather_forecast(self):
        self.database_adapt.execute(queries.DELETE_ALL_HOURLY_FORECAST)

    def delete_all_from_daily_weather_forecast(self):
        self.database_adapt.execute(queries.DELETE_ALL_DAILY_FORECAST)

    def __repr__(self):
        return f"{type(self).__name__}(database_adapt={self.database_adapt!r})"
