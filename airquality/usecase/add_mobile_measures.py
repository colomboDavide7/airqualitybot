######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 11:54
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import logging
from datetime import datetime
from typing import Dict, List
import airquality.environment as environ
from airquality.extra.timest import Timest
from airquality.datamodel.apiparam import APIParam
from airquality.database.gateway import DatabaseGateway
from airquality.url.api_server_wrap import APIServerWrapper
from airquality.extra.logger_extra import FileHandlerRotator
from airquality.url.timeiter_url import AtmotubeTimeIterableURL
from airquality.core.apidata_builder import AtmotubeAPIDataBuilder
from airquality.core.request_builder import AddAtmotubeMeasureRequestBuilder
from airquality.core.request_validator import AddSensorMeasuresRequestValidator
from airquality.core.response_builder import AddMobileMeasureResponseBuilder


class AddAtmotubeMeasures(object):
    """
    A *UsecaseRunner* that defines how to run the *AddMobileMeasures* UseCase.
    """

    def __init__(
        self,
        database_gway: DatabaseGateway,
        server_wrap: APIServerWrapper,
        timest: Timest
    ):
        self._timest = timest
        self._database_gway = database_gway
        self._server_wrap = server_wrap
        self._environ = environ.get_environ()
        self._logger = logging.getLogger(__name__)
        self._file_handler_rotator = None
        self._cached_url_template = ""

    def _database_measure_param(self) -> Dict[str, int]:
        return self._database_gway.query_measure_param_owned_by(
            owner="atmotube"
        )

    def _database_api_param(self) -> List[APIParam]:
        return self._database_gway.query_sensor_apiparam_of_type(
            sensor_type="atmotube"
        )

    def _packet_id(self) -> int:
        return self._database_gway.query_max_mobile_packet_id_plus_one()

    def _filter_ts_of(self, api_param: APIParam) -> datetime:
        """
        This method is called to get the timestamp used to filter out old measures before inserting into the database.

        :param api_param:                       the API param to search for the 'last_acquisition' timestamp.
        :return:                                the 'last_acquisition' datetime-aware object from the database.
        """
        return self._database_gway.query_last_acquisition_of(
            sensor_id=api_param.sensor_id,
            ch_name=api_param.ch_name
        )

    def _url_template(self) -> str:
        if not self._cached_url_template:
            self._cached_url_template = self._environ.url_template(personality='atmotube')
        return self._cached_url_template

    def _urls_of(self, api_param: APIParam) -> AtmotubeTimeIterableURL:
        pre_formatted_url = self._url_template().format(
            api_key=api_param.api_key,
            api_id=api_param.api_id,
            api_fmt="json"
        )
        return AtmotubeTimeIterableURL(
            url=pre_formatted_url,
            begin=api_param.last_acquisition,
            step_size_in_days=1
        )

    def _safe_rotate_handler(self, sensor_id: int):
        if self._file_handler_rotator is None:
            self._file_handler_rotator = FileHandlerRotator(
                logger_name=self._logger.name,
                logger_level=self._logger.level,
                logger_dir=self._environ.logging_dir_of(personality='atmotube')
            )
        sensor_ident = self._database_gway.query_mobile_sensor_unique_info(
            sensor_id=sensor_id
        )
        self._file_handler_rotator.rotate(
            sensor_ident=sensor_ident
        )

# =========== SAFE METHODS
    def _safe_insert(self, validator: AddSensorMeasuresRequestValidator, api_param: APIParam):
        if validator:
            self._logger.debug(
                "found #%d responses within: [%s - %s]" %
                (len(validator), validator[0].timestamp, validator[-1].timestamp)
            )

            response_builder = AddMobileMeasureResponseBuilder(
                requests=validator,
                start_packet_id=self._packet_id()
            )
            self._logger.debug("found #%d responses" % len(response_builder))

            self._database_gway.insert_mobile_measures(responses=response_builder)
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
    def run(self):
        measure_param = self._database_measure_param()
        self._logger.debug("parameters in use for mapping the measures with database code => %s" % repr(measure_param))

        for param in self._database_api_param():
            self._safe_rotate_handler(sensor_id=param.sensor_id)
            self._logger.debug("parameters in use for fetching sensor data => %s" % repr(param))

            for url in self._urls_of(param):
                self._logger.debug("downloading sensor measures at => %s" % url)

                server_jresp = self._server_wrap.json(url=url)
                self._logger.debug("successfully get server response!!!")

                datamodel_builder = AtmotubeAPIDataBuilder(json_response=server_jresp)
                self._logger.debug("found #%d API data" % len(datamodel_builder))

                request_builder = AddAtmotubeMeasureRequestBuilder(
                    datamodel=datamodel_builder,
                    timest=self._timest,
                    code2id=measure_param
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
