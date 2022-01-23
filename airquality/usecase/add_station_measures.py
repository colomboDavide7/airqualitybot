######################################################
#
# Author: Davide Colombo
# Date: 01/01/22 16:53
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import logging
from typing import List, Dict
from datetime import datetime
import airquality.environment as env
from airquality.datamodel.timest import Timest
from airquality.datamodel.apiparam import APIParam
from airquality.database.gateway import DatabaseGateway
from airquality.url.api_server_wrap import APIServerWrapper
from airquality.extra.logger_extra import FileHandlerRotator
from airquality.url.timeiter_url import ThingspeakTimeIterableURL
from airquality.core.apidata_builder import ThingspeakAPIDataBuilder
from airquality.core.request_builder import AddThingspeakMeasuresRequestBuilder
from airquality.core.request_validator import AddSensorMeasuresRequestValidator
from airquality.core.response_builder import AddStationMeasuresResponseBuilder


class AddThingspeakMeasures(object):
    """
    An *object* that defines the application UseCase of adding the measures detected by a fixed sensor (i.e., a station)

    Data are fetched from the API by building a set of urls by covering the period from the *last_acquisition* (queried
    from the database) to the moment of the application running.

    At each cycle, if there are new measures these are inserted into the database and the *last_acquisition* timestamp
    is updated to the timestamp of the last measure successfully inserted.
    """

    MAPPING_1A = {'field1': 'pm1.0_atm_a', 'field2': 'pm2.5_atm_a', 'field3': 'pm10.0_atm_a', 'field6': 'temperature_a',
                  'field7': 'humidity_a'}
    MAPPING_1B = {'field1': 'pm1.0_atm_b', 'field2': 'pm2.5_atm_b', 'field3': 'pm10.0_atm_b', 'field6': 'pressure_b'}
    MAPPING_2A = {'field1': '0.3_um_count_a', 'field2': '0.5_um_count_a', 'field3': '1.0_um_count_a',
                  'field4': '2.5_um_count_a', 'field5': '5.0_um_count_a', 'field6': '10.0_um_count_a'}
    MAPPING_2B = {'field1': '0.3_um_count_b', 'field2': '0.5_um_count_b', 'field3': '1.0_um_count_b',
                  'field4': '2.5_um_count_b', 'field5': '5.0_um_count_b', 'field6': '10.0_um_count_b'}
    FIELD_MAP = {'1A': MAPPING_1A, '1B': MAPPING_1B, '2A': MAPPING_2A, '2B': MAPPING_2B}

    def __init__(
        self,
        database_gway: DatabaseGateway,
        server_wrap: APIServerWrapper,
        timest: Timest
    ):
        self._timest = timest                               # the date and time handler class.
        self._database_gway = database_gway                 # the gateway interface for storing data into database.
        self._server_wrap = server_wrap                     # the instance that handles download of the sensor data.
        self._environ = env.get_environ()                   # the Singleton Environment instance.
        self._logger = logging.getLogger(__name__)          # the Logger instance.
        self._file_handler_rotator = None                   # the file handler rotator associated to the current logger.
        self._cached_url_template = ""                      # the cached URL template for fetching sensor data.

    def _database_measure_param(self) -> Dict[str, int]:
        return self._database_gway.query_measure_param_owned_by(
            owner="thingspeak"
        )

    def _database_api_param(self) -> List[APIParam]:
        return self._database_gway.query_sensor_apiparam_of_type(
            sensor_type="thingspeak"
        )

    def _packet_id(self) -> int:
        return self._database_gway.query_max_station_packet_id_plus_one()

    def _fields_of(self, param: APIParam) -> Dict[str, str]:
        return self.FIELD_MAP[param.ch_name]

    def _filter_ts_of(self, param: APIParam) -> datetime:
        return self._database_gway.query_last_acquisition_of(
            sensor_id=param.sensor_id,
            ch_name=param.ch_name
        )

    def _url_template(self):
        if not self._cached_url_template:
            self._cached_url_template = self._environ.url_template(personality='thingspeak')
        return self._cached_url_template

    def _urls_of(self, param: APIParam) -> ThingspeakTimeIterableURL:
        pre_formatted_url = self._url_template().format(
            api_key=param.api_key,
            api_id=param.api_id,
            api_fmt="json"
        )
        return ThingspeakTimeIterableURL(
            url=pre_formatted_url,
            begin=param.last_acquisition,
            step_size_in_days=7
        )

    def _safe_rotate_handler(self, sensor_ident):
        """
        This function lazy initialize the file handler rotator (if no one already exists) and rotate the file handler.
        """

        if self._file_handler_rotator is None:
            self._file_handler_rotator = FileHandlerRotator(
                logger_name=self._logger.name,
                logger_level=self._logger.level,
                logger_dir=self._environ.logging_dir_of(personality='thingspeak')
            )
        self._file_handler_rotator.rotate(
            sensor_ident=sensor_ident
        )

# =========== SAFE METHODS
    def _safe_insert(self, validator: AddSensorMeasuresRequestValidator, api_param: APIParam):
        if validator:
            self._logger.debug(
                "found responses within: [%s - %s]" %
                (validator[0].timestamp, validator[-1].timestamp)
            )

            response_builder = AddStationMeasuresResponseBuilder(
                requests=validator,
                start_packet_id=self._packet_id(),
                sensor_id=api_param.sensor_id
            )
            self._logger.debug("found #%d responses" % len(response_builder))

            self._database_gway.insert_station_measures(responses=response_builder)
            self._safe_update(
                time=validator[-1].timestamp,
                api_param=api_param
            )

    def _safe_update(self, time: datetime, api_param: APIParam):
        self._logger.debug("updating last acquisition timestamp to => '%s'" % time)
        self._database_gway.update_last_acquisition_of(
            timestamp=time,
            sensor_id=api_param.sensor_id,
            ch_name=api_param.ch_name
        )

# =========== RUN METHOD
    def run(self) -> None:
        measure_param = self._database_measure_param()
        self._logger.debug("parameters in use for mapping the measures with database code => %s" % repr(measure_param))

        for param in self._database_api_param():
            self._logger.debug("parameters in use for fetching sensor data => %s" % repr(param))

            sensor_ident = self._database_gway.query_fixed_sensor_unique_info(
                sensor_id=param.sensor_id
            )
            self._safe_rotate_handler(sensor_ident=sensor_ident)

            for url in self._urls_of(param):
                self._logger.debug("downloading sensor measures at => %s" % url)

                server_jresp = self._server_wrap.json(url=url)
                self._logger.debug("successfully get server response!!!")

                datamodel_builder = ThingspeakAPIDataBuilder(json_response=server_jresp)
                self._logger.debug("found #%d API data" % len(datamodel_builder))

                request_builder = AddThingspeakMeasuresRequestBuilder(
                    datamodel=datamodel_builder,
                    timest=self._timest,
                    code2id=measure_param,
                    field_map=self._fields_of(param)
                )
                self._logger.debug("found #%d requests" % len(request_builder))

                validator = AddSensorMeasuresRequestValidator(
                    request=request_builder,
                    filter_ts=self._filter_ts_of(param)
                )

                self._safe_insert(
                    validator=validator,
                    api_param=param
                )
