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
from airquality.datamodel.geolocation import Geolocation
from airquality.datamodel.sensor_ident import SensorIdentity
from airquality.datamodel.openweathermap_key import OpenweathermapKey
from airquality.datamodel.apidata import WeatherCityData, CityOfGeoarea
from airquality.extra.decorators import throw_on, constructor, index, dict_from_tuples
from airquality.core.response_builder import \
    AddFixedSensorResponseBuilder, \
    AddMobileMeasureResponseBuilder, \
    AddStationMeasuresResponseBuilder, \
    AddPlacesResponseBuilder, \
    AddOpenWeatherMapDataResponseBuilder


class DatabaseGateway(object):
    """
    A class that defines how the application can interact with the database.

    This class defines all the queries that the application can perform against the database.

    It supports SELECT, INSERT, UPDATE and DELETE.

    """

    def __init__(self, database_adapt: DatabaseAdapter):
        self.database_adapt = database_adapt
        self._logger = logging.getLogger(__name__)

    def _safe_fetch_id(self, query: str):
        row = self.database_adapt.fetchone(query)
        return 1 if row[0] is None else row[0] + 1

# =========== SELECT ID QUERIES
    def query_max_sensor_id_plus_one(self) -> int:
        return self._safe_fetch_id(
            query=queries.SELECT_MAX_SENS_ID
        )

    def query_max_mobile_packet_id_plus_one(self) -> int:
        return self._safe_fetch_id(
            query=queries.SELECT_MAX_MOBILE_PACK_ID
        )

    def query_max_station_packet_id_plus_one(self) -> int:
        return self._safe_fetch_id(
            query=queries.SELECT_MAX_STATION_PACK_ID
        )

# =========== SELECT SET QUERIES
    def query_poscodes_of_country(self, country_code: str) -> Set[str]:
        rows = self.database_adapt.fetchall(
            query=queries.SELECT_POSCODES_OF.format(code=country_code)
        )
        return {row[0] for row in rows}

    def query_sensor_names_of_type(self, sensor_type: str) -> Set[str]:
        rows = self.database_adapt.fetchall(
            query=queries.SELECT_SENSOR_NAMES.format(type=sensor_type)
        )
        return {row[0] for row in rows}

# =========== SELECT MAPPING QUERIES
    @dict_from_tuples(key_index=1)
    @throw_on(sentinel_value=[], exc_cls=ValueError)
    def query_measure_param_owned_by(self, owner: str) -> Dict[str, int]:
        return self.database_adapt.fetchall(
            query=queries.SELECT_MEASURE_PARAM.format(owner=owner)
        )

# =========== SELECT LIST QUERIES
    @throw_on(sentinel_value=[], exc_cls=ValueError)
    def query_sensor_apiparam_of_type(self, sensor_type: str) -> List[APIParam]:
        rows = self.database_adapt.fetchall(
            query=queries.SELECT_SENS_API_PARAM_OF.format(type=sensor_type)
        )
        return [
            APIParam(sensor_id=sid, api_key=key, api_id=ident, ch_name=name, last_acquisition=last) for
            sid, key, ident, name, last in rows
        ]

    @throw_on(sentinel_value=[], exc_cls=ValueError)
    def query_openweathermap_keys(self) -> List[OpenweathermapKey]:
        rows = self.database_adapt.fetchall(
            query=queries.SELECT_OPENWEATHERMAP_KEY
        )
        return [
            OpenweathermapKey(
                key_value=key_val,
                done_requests_per_minute=done_r,
                max_requests_per_minute=max_r
            ) for key_val, done_r, max_r in rows]

    @throw_on(sentinel_value=[], exc_cls=ValueError)
    def query_weather_conditions(self):
        return self.database_adapt.fetchall(
            query=queries.SELECT_WEATHER_COND
        )

# =========== SELECT SINGLE ROW QUERIES
    @index(idx=0)
    @throw_on(sentinel_value=None, exc_cls=ValueError)
    def query_last_acquisition_of(self, sensor_id: int, ch_name: str) -> datetime:
        return self.database_adapt.fetchone(
            query=queries.SELECT_LAST_ACQUISITION_OF.format(sid=sensor_id, ch=ch_name)
        )

    @constructor(cls=CityOfGeoarea)
    @throw_on(sentinel_value=None, exc_cls=ValueError)
    def query_geolocation_of(self, city: WeatherCityData):
        return self.database_adapt.fetchone(
            query=queries.SELECT_GEOLOCATION_OF.format(country=city.country_code, place=city.place_name)
        )

    @constructor(cls=SensorIdentity)
    @throw_on(sentinel_value=None, exc_cls=ValueError)
    def query_fixed_sensor_unique_info(self, sensor_id: int):
        return self.database_adapt.fetchone(
            query=queries.SELECT_FIXED_SENSOR_UNIQUE_INFO.format(sid=sensor_id)
        )

    @constructor(cls=SensorIdentity)
    @throw_on(sentinel_value=None, exc_cls=ValueError)
    def query_mobile_sensor_unique_info(self, sensor_id: int):
        return self.database_adapt.fetchone(
            query=queries.SELECT_MOBILE_SENSOR_UNIQUE_INFO.format(sid=sensor_id)
        )

    @constructor(cls=Geolocation)
    @throw_on(sentinel_value=None, exc_cls=ValueError)
    def query_purpleair_location(self, sensor_index: int):
        return self.database_adapt.fetchone(
            query=queries.SELECT_PURPLEAIR_LOCATION.format(idx=sensor_index)
        )

# =========== INSERT QUERIES
    def _safe_format_insert_query(self, query: str, values: str) -> str:
        """
        A method that safely format insert queries by checking that values is not empty.

        :param query:           the insert query to be formatted IT MUST CONTAIN THE *val* KEYWORD ARGUMENT.
        :param values:          the values to format the query with.
        :return:                the original query formatted or empty string.
        """

        if values:
            return query.format(val=values)
        self._logger.warning(f"[CAUSE]: failed to format insert query - [QUERY]: {query} - [VALUES]: '{values}'")
        return ""

    def insert_weather_data(self, responses: AddOpenWeatherMapDataResponseBuilder):
        """
        A method that knows how to build the query for inserting weather data including current weather,
        hourly forecast, daily forecast and weather alerts.

        :param responses:               the response builder instance that generates the weather responses.
        """

        cval = hval = dval = aval = ""
        for r in responses:
            cval += f"{r.current_weather_record},"
            hval += f"{r.hourly_forecast_record},"
            dval += f"{r.daily_forecast_record},"
            aval += f"{r.weather_alert_record},"
        query = self._safe_format_insert_query(query=queries.INSERT_CURRENT_WEATHER_DATA, values=cval.strip(','))
        query += self._safe_format_insert_query(query=queries.INSERT_HOURLY_FORECAST_DATA, values=hval.strip(','))
        query += self._safe_format_insert_query(query=queries.INSERT_DAILY_FORECAST_DATA, values=dval.strip(','))
        query += self._safe_format_insert_query(query=queries.INSERT_WEATHER_ALERT_DATA, values=aval.strip(','))
        self.database_adapt.execute(query)

    def insert_sensors(self, responses: AddFixedSensorResponseBuilder):
        """
        A method that knows how to build the query for inserting sensor data including sensor basic information,
        sensor API param and sensor geolocation.

        :param responses:               the response builder instance that generates the weather responses.
        """

        sval = pval = ""
        for r in responses:
            sval += f"{r.sensor_record},"
            pval += f"{r.apiparam_record},"
        query = self._safe_format_insert_query(query=queries.INSERT_SENSORS, values=sval.strip(','))
        query += self._safe_format_insert_query(query=queries.INSERT_SENSOR_API_PARAM, values=pval.strip(','))
        self.database_adapt.execute(query)

    def insert_mobile_measures(self, responses: AddMobileMeasureResponseBuilder):
        """
        A method that knows how to build the query for inserting mobile sensor's measures.

        :param responses:           the response builder instance that generates the mobile sensor's measure responses.
        """

        query = self._safe_format_insert_query(
            query=queries.INSERT_MOBILE_MEASURES,
            values=','.join(resp.measure_record for resp in responses)
        )
        self.database_adapt.execute(query)

    def insert_station_measures(self, responses: AddStationMeasuresResponseBuilder):
        """
        A method that knows how to build the query for inserting fixed sensor's measures.

        :param responses:           the response builder instance that generates the fixed sensor's measure responses.
        """

        query = self._safe_format_insert_query(
            query=queries.INSERT_STATION_MEASURES,
            values=','.join(resp.measure_record for resp in responses)
        )
        self.database_adapt.execute(query)

    def insert_places(self, responses: AddPlacesResponseBuilder):
        """
        A method that knows how to build the query for inserting country locations.

        :param responses:           the response builder instance that generates the country location responses.
        """

        query = self._safe_format_insert_query(
            query=queries.INSERT_PLACES,
            values=','.join(resp.place_record for resp in responses)
        )
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
        return f"{type(self).__name__}"
