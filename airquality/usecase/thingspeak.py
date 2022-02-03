######################################################
#
# Author: Davide Colombo
# Date: 01/01/22 16:53
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import logging
import airquality.environment as environ
from airquality.extra.logging import FileHandlerRotator

_ENVIRON = environ.get_environ()
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)
_FILE_ROTATOR = FileHandlerRotator(
    logger_name=_LOGGER.name,
    logger_level=_LOGGER.level,
    logger_dir=_ENVIRON.logging_dir_of(personality='thingspeak')
)

######################################################
from datetime import datetime
import airquality.usecase as constants
from airquality.usecase.abc import UsecaseABC
from airquality.extra.decorator import log_context
from airquality.extra.url import json_http_response
from airquality.database.gateway import DatabaseGateway
from airquality.datamodel.fromdb import SensorApiParamDM
from airquality.iterables.urls import ThingspeakIterableUrls
from airquality.iterables.fromapi import ThingspeakIterableDatamodels
from airquality.iterables.requests import ThingspeakIterableRequests
from airquality.iterables.validator import SensorMeasureIterableValidRequests
from airquality.iterables.responses import StationMeasureIterableResponses


class Thingspeak(UsecaseABC):
    """
    A class that implements the *UsecaseABC* and defines the business rules for downloading, transforming and
    storing sensor measures from the Thingspeak API.
    """

    _MAPPING_1A = {'field1': 'pm1.0_atm_a', 'field2': 'pm2.5_atm_a', 'field3': 'pm10.0_atm_a',
                   'field6': 'temperature_a',
                   'field7': 'humidity_a'}
    _MAPPING_1B = {'field1': 'pm1.0_atm_b', 'field2': 'pm2.5_atm_b', 'field3': 'pm10.0_atm_b', 'field6': 'pressure_b'}
    _MAPPING_2A = {'field1': '0.3_um_count_a', 'field2': '0.5_um_count_a', 'field3': '1.0_um_count_a',
                   'field4': '2.5_um_count_a', 'field5': '5.0_um_count_a', 'field6': '10.0_um_count_a'}
    _MAPPING_2B = {'field1': '0.3_um_count_b', 'field2': '0.5_um_count_b', 'field3': '1.0_um_count_b',
                   'field4': '2.5_um_count_b', 'field5': '5.0_um_count_b', 'field6': '10.0_um_count_b'}
    _FIELD_MAP = {'1A': _MAPPING_1A, '1B': _MAPPING_1B, '2A': _MAPPING_2A, '2B': _MAPPING_2B}

    def __init__(self, database_gway: DatabaseGateway):
        self._database_gway = database_gway
        self._url_template = _ENVIRON.url_template(personality='thingspeak')
        self._measure_param = self._database_gway.query_measure_param_owned_by(owner="thingspeak")
        self._api_param = self._database_gway.query_sensor_apiparam_of_type(sensor_type="thingspeak")

    def _packet_id(self) -> int:
        return self._database_gway.query_max_station_packet_id_plus_one()

    def _filter_ts_of(self, param: SensorApiParamDM) -> datetime:
        return self._database_gway.query_last_acquisition_of(
            sensor_id=param.sensor_id,
            ch_name=param.ch_name
        )

    def _urls_of(self, param: SensorApiParamDM) -> ThingspeakIterableUrls:
        pre_formatted_url = self._url_template.format(
            api_key=param.api_key,
            api_id=param.api_id,
            api_fmt="json"
        )
        return ThingspeakIterableUrls(
            url=pre_formatted_url,
            begin=param.last_acquisition,
            step_size_in_days=7
        )

    def _rotate_file(self, sensor_id: int):
        sensor_ident = self._database_gway.query_fixed_sensor_unique_info(sensor_id=sensor_id)
        _FILE_ROTATOR.rotate(sensor_ident=sensor_ident)

# =========== EXECUTE METHOD
    def execute(self):
        for param in self._api_param:
            self._rotate_file(sensor_id=param.sensor_id)
            self._safe_execute(param=param)

    @log_context(logger_name=__name__, header=constants.START_MESSAGE, teardown=constants.END_MESSAGE)
    def _safe_execute(self, param: SensorApiParamDM):
        _LOGGER.debug("%s" % repr(param))
        for url in self._urls_of(param):
            server_jresp = json_http_response(url=url)
            datamodels = ThingspeakIterableDatamodels(json_response=server_jresp)
            requests = ThingspeakIterableRequests(
                datamodels=datamodels, measure_param=self._measure_param, api_field_names=self._FIELD_MAP[param.ch_name]
            )
            valid_requests = SensorMeasureIterableValidRequests(
                requests=requests, filter_ts=self._filter_ts_of(param)
            )
            if not valid_requests:
                _LOGGER.debug('no valid measures found.')
                continue

            responses = StationMeasureIterableResponses(
                requests=valid_requests, sensor_param=param, start_packet_id=self._packet_id()
            )

            self._database_gway.execute(query=responses.query())
            _LOGGER.debug("inserted %d/%d measures" % (len(valid_requests), len(datamodels)))
