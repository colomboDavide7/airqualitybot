######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 11:54
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
    logger_dir=_ENVIRON.logging_dir_of(personality='atmotube')
)

######################################################
from datetime import datetime
import airquality.usecase as constants
from airquality.usecase.abc import UsecaseABC
from airquality.extra.decorator import log_context
from airquality.extra.url import json_http_response
from airquality.database.gateway import DatabaseGateway
from airquality.datamodel.fromdb import SensorApiParamDM
from airquality.iterables.urls import AtmotubeIterableUrls
from airquality.iterables.fromapi import AtmotubeIterableDatamodels
from airquality.iterables.requests import AtmotubeIterableRequests
from airquality.iterables.validator import SensorMeasureIterableValidRequests
from airquality.iterables.responses import MobileMeasureIterableResponses


class Atmotube(UsecaseABC):
    """
    A class that implements the *UsecaseABC* and defines the business rules for downloading, transforming and
    storing sensor measures from the Atmotube API.
    """

    def __init__(self, database_gway: DatabaseGateway):
        self._database_gway = database_gway
        self._url_template = _ENVIRON.url_template(personality='atmotube')
        self._measure_param = self._database_gway.query_measure_param_owned_by(owner="atmotube")
        self._api_param = self._database_gway.query_sensor_apiparam_of_type(sensor_type="atmotube")

    def _packet_id(self) -> int:
        return self._database_gway.query_max_mobile_packet_id_plus_one()

    def _filter_ts_of(self, api_param: SensorApiParamDM) -> datetime:
        return self._database_gway.query_last_acquisition_of(
            sensor_id=api_param.sid,
            ch_name=api_param.ch
        )

    def _urls_of(self, api_param: SensorApiParamDM) -> AtmotubeIterableUrls:
        pre_formatted_url = self._url_template.format(
            api_key=api_param.key,
            api_id=api_param.id,
            api_fmt="json"
        )
        return AtmotubeIterableUrls(
            url=pre_formatted_url,
            begin=api_param.last,
            step_size_in_days=1
        )

    def _rotate_file(self, sensor_id: int):
        sensor_ident = self._database_gway.query_mobile_sensor_unique_info(sensor_id=sensor_id)
        _FILE_ROTATOR.rotate(sensor_ident=sensor_ident)

# =========== RUN METHOD
    def execute(self):
        for param in self._api_param:
            self._rotate_file(sensor_id=param.sid)
            self._safe_execute(param=param)

    @log_context(logger_name=__name__, header=constants.START_MESSAGE, teardown=constants.END_MESSAGE)
    def _safe_execute(self, param: SensorApiParamDM):
        _LOGGER.debug("%s" % repr(param))
        for url in self._urls_of(param):
            server_jresp = json_http_response(url=url)
            datamodels = AtmotubeIterableDatamodels(json_response=server_jresp)
            requests = AtmotubeIterableRequests(datamodels=datamodels, measure_param=self._measure_param)
            valid_requests = SensorMeasureIterableValidRequests(requests=requests, filter_ts=self._filter_ts_of(param))
            if not valid_requests:
                _LOGGER.debug('no valid measures found.')
                continue

            responses = MobileMeasureIterableResponses(
                requests=valid_requests, start_packet_id=self._packet_id(), sensor_param=param
            )
            self._database_gway.execute(query=responses.query())
            _LOGGER.debug("inserted %d/%d measures" % (len(valid_requests), len(datamodels)))
