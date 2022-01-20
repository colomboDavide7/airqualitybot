######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 15:01
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.core.response_builder import AddFixedSensorResponseBuilder, AddMobileMeasureResponseBuilder, \
    AddStationMeasuresResponseBuilder, AddPlacesResponseBuilder, AddOpenWeatherMapDataResponseBuilder
from airquality.database.adapter import DatabaseAdapter
from airquality.datamodel.apidata import WeatherCityData, CityOfGeoarea
from airquality.datamodel.apiparam import APIParam
from airquality.datamodel.service_param import ServiceParam
from typing import Set, Dict, List
from datetime import datetime
import airquality.database as const
import logging


class DatabaseGateway(object):
    """
    A class that defines how the application can interact with the database.

    Every single query that can be executed must be defined here within a method.

    Keyword arguments:
        *database_adapt*            the concrete implementation of DatabaseAdapter interface for executing actions
                                    agains the database.

    """

    def __init__(self, database_adapt: DatabaseAdapter):
        self.database_adapt = database_adapt
        self._logger = logging.getLogger(__name__)

    def _raise(self, cause: str):
        self._logger.exception(cause)
        raise ValueError(cause)

# ================================= #
#                                   #
# MEASURE PARAM TABLE
#                                   #
# ================================= #
    def get_measure_param_owned_by(self, owner: str) -> Dict[str, int]:
        rows = self.database_adapt.fetchall(const.SELECT_MEASURE_PARAM.format(owner=owner))
        if not rows:
            self._raise(f"[FATAL]: database failed to query 'measure_param' owned by '{owner}'!!!")
        return {code: ident for ident, code in rows}

# ================================= #
#                                   #
# SENSOR TABLE
#                                   #
# ================================= #
    def get_existing_sensor_names_of_type(self, sensor_type: str) -> Set[str]:
        return {row[0] for row in self.database_adapt.fetchall(const.SELECT_SENSOR_NAMES.format(type=sensor_type))}

    def get_max_sensor_id_plus_one(self) -> int:
        row = self.database_adapt.fetchone(const.SELECT_MAX_SENS_ID)
        return 1 if row[0] is None else row[0] + 1

    def insert_sensors(self, responses: AddFixedSensorResponseBuilder):
        sval = pval = gval = ""
        for r in responses:
            sval += f"{r.sensor_record},"
            pval += f"{r.apiparam_record},"
            gval += f"{r.geolocation_record},"
        sensor_query = const.INSERT_SENSORS.format(val=sval.strip(','))
        apiparam_query = const.INSERT_SENSOR_API_PARAM.format(val=pval.strip(','))
        geolocation_query = const.INSERT_SENSOR_LOCATION.format(val=gval.strip(','))
        self.database_adapt.execute(f"{sensor_query} {apiparam_query} {geolocation_query}")

# ================================= #
#                                   #
# SENSOR API PARAM TABLE
#                                   #
# ================================= #
    def get_last_acquisition_of(self, sensor_id: int, ch_name: str) -> datetime:
        row = self.database_adapt.fetchone(const.SELECT_LAST_ACQUISITION_OF.format(sid=sensor_id, ch=ch_name))
        if row is None:
            self._raise(f"[FATAL]: database failed to query 'sensor_api_param': "
                        f"sensor_id='{sensor_id}', ch_name='{ch_name}'!!!")
        return row[0]

    def get_sensor_apiparam_of_type(self, sensor_type: str) -> List[APIParam]:
        rows = self.database_adapt.fetchall(const.SELECT_SENS_API_PARAM_OF.format(type=sensor_type))
        if not rows:
            self._raise(f"[FATAL]: database failed to query 'sensor_api_param' of sensor type '{sensor_type}'!!!")
        return [APIParam(sensor_id=sid,
                         api_key=key,
                         api_id=ident,
                         ch_name=name,
                         last_acquisition=last) for sid, key, ident, name, last in rows]

    def update_last_acquisition_of(self, timestamp: datetime, sensor_id: int, ch_name: str):
        self.database_adapt.execute(const.UPDATE_LAST_CH_TIMEST.format(time=timestamp, sid=sensor_id, ch=ch_name))

# ================================= #
#                                   #
# MOBILE MEASUREMENTS TABLE
#                                   #
# ================================= #
    def get_max_mobile_packet_id_plus_one(self) -> int:
        row = self.database_adapt.fetchone(const.SELECT_MAX_MOBILE_PACK_ID)
        return 1 if row[0] is None else row[0] + 1

    def insert_mobile_measures(self, responses: AddMobileMeasureResponseBuilder):
        values = ','.join(resp.measure_record for resp in responses)
        measure_query = const.INSERT_MOBILE_MEASURES.format(val=values)
        self.database_adapt.execute(measure_query)

# ================================= #
#                                   #
# STATION MEASUREMENT TABLE
#                                   #
# ================================= #
    def get_max_station_packet_id_plus_one(self) -> int:
        row = self.database_adapt.fetchone(const.SELECT_MAX_STATION_PACK_ID)
        return 1 if row[0] is None else row[0] + 1

    def insert_station_measures(self, responses: AddStationMeasuresResponseBuilder):
        values = ','.join(resp.measure_record for resp in responses)
        query = const.INSERT_STATION_MEASURES.format(val=values)
        self.database_adapt.execute(query)

# ================================= #
#                                   #
# SERVICE TABLE
#                                   #
# ================================= #
    def get_service_id_from_name(self, service_name: str) -> int:
        row = self.database_adapt.fetchone(const.SELECT_SERVICE_ID_FROM.format(sn=service_name))
        if row is None:
            self._raise(f"[FATAL]: database failed to query 'service_id' for service '{service_name}'!!!")
        return row[0]

# ================================= #
#                                   #
# SERVICE API PARAM TABLE
#                                   #
# ================================= #
    def get_service_apiparam_of(self, service_name: str) -> List[ServiceParam]:
        rows = self.database_adapt.fetchall(const.SELECT_SERVICE_API_PARAM_OF.format(sn=service_name))
        if not rows:
            self._raise(f"[FATAL]: database failed to query 'service_api_param' for service '{service_name}'!!!")
        return [ServiceParam(api_key=api_key, n_requests=nreq) for api_key, nreq in rows]

# ================================= #
#                                   #
# GEOGRAPHICAL AREA TABLE
#                                   #
# ================================= #
    def get_poscodes_of_country(self, country_code: str) -> Set[str]:
        return {row[0] for row in self.database_adapt.fetchall(const.SELECT_POSCODES_OF.format(code=country_code))}

    def insert_places(self, responses: AddPlacesResponseBuilder):
        values = ','.join(resp.place_record for resp in responses)
        query = const.INSERT_PLACES.format(val=values)
        self.database_adapt.execute(query)

    def get_geolocation_of(self, city: WeatherCityData) -> CityOfGeoarea:
        row = self.database_adapt.fetchone(
            const.SELECT_GEOLOCATION_OF.format(country=city.country_code, place=city.place_name)
        )
        if row is None:
            self._raise(f"[FATAL]: database failed to query 'geographical_area' from {city!r}!!!")
        return CityOfGeoarea(geoarea_id=row[0], longitude=row[1], latitude=row[2])

# ================================= #
#                                   #
# WEATHER CONDITION TABLE
#                                   #
# ================================= #
    def get_weather_conditions(self):
        rows = self.database_adapt.fetchall(const.SELECT_WEATHER_COND)
        if not rows:
            self._raise(f"[FATAL]: database failed to query 'weather_condition'!!!")
        return rows

# ================================= #
#                                   #
# HOURLY FORECAST TABLE
#                                   #
# ================================= #
    def delete_all_from_hourly_weather_forecast(self):
        self.database_adapt.execute(const.DELETE_ALL_HOURLY_FORECAST)

# ================================= #
#                                   #
# DAILY FORECAST TABLE
#                                   #
# ================================= #
    def delete_all_from_daily_weather_forecast(self):
        self.database_adapt.execute(const.DELETE_ALL_DAILY_FORECAST)

# ================================= #
#                                   #
# CURRENT WEATHER TABLE
#                                   #
# ================================= #
    def insert_weather_data(self, responses: AddOpenWeatherMapDataResponseBuilder):
        cval = hval = dval = ""
        for r in responses:
            cval += f"{r.current_weather_record},"
            hval += f"{r.hourly_forecast_record},"
            dval += f"{r.daily_forecast_record},"
        current_weather_query = const.INSERT_CURRENT_WEATHER_DATA.format(val=cval.strip(','))
        hourly_forecast_query = const.INSERT_HOURLY_FORECAST_DATA.format(val=hval.strip(','))
        daily_forecast_query = const.INSERT_DAILY_FORECAST_DATA.format(val=dval.strip(','))
        self.database_adapt.execute(f"{current_weather_query} {hourly_forecast_query} {daily_forecast_query}")

    def __repr__(self):
        return f"{type(self).__name__}(database_adapt={self.database_adapt!r})"
