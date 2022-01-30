######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 11:54
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import logging
from datetime import datetime
import airquality.usecase as constants
import airquality.environment as environ
from airquality.usecase.abc import UsecaseABC
from airquality.extra.timest import atmotube_timest
from airquality.datamodel.apiparam import APIParam
from airquality.database.gateway import DatabaseGateway
from airquality.url.url_reader import json_http_response
from airquality.extra.logger_extra import FileHandlerRotator
from airquality.url.timeiter_url import AtmotubeTimeIterableURL
from airquality.core.apidata_builder import AtmotubeAPIDataBuilder
from airquality.core.request_builder import AddAtmotubeMeasureRequestBuilder
from airquality.core.request_validator import AddSensorMeasuresRequestValidator
from airquality.core.response_builder import AddMobileMeasureResponseBuilder

_ENVIRON = environ.get_environ()
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)
_FILE_ROTATOR = FileHandlerRotator(
    logger_name=_LOGGER.name,
    logger_level=_LOGGER.level,
    logger_dir=_ENVIRON.logging_dir_of(personality='atmotube')
)
_TIMEST = atmotube_timest()


def _build_insert_query(response_builder: AddMobileMeasureResponseBuilder) -> str:
    return "INSERT INTO level0_raw.mobile_measurement " \
           "(packet_id, param_id, param_value, timestamp, geom) " \
           f"VALUES {','.join(resp.measure_record for resp in response_builder)};"


def _build_update_query(time: datetime, sensor_id: int, channel_name: str) -> str:
    return "UPDATE level0_raw.sensor_api_param " \
           f"SET last_acquisition = '{time}' " \
           f"WHERE sensor_id = {sensor_id} AND ch_name = '{channel_name}';"


class AddAtmotubeMeasures(UsecaseABC):
    def __init__(self, database_gway: DatabaseGateway):
        self._database_gway = database_gway
        self._measure_param = self._database_gway.query_measure_param_owned_by(owner="atmotube")
        self._api_param = self._database_gway.query_sensor_apiparam_of_type(sensor_type="atmotube")
        self._cached_url_template = _ENVIRON.url_template(personality='atmotube')

    def _packet_id(self) -> int:
        return self._database_gway.query_max_mobile_packet_id_plus_one()

    def _filter_ts_of(self, api_param: APIParam) -> datetime:
        return self._database_gway.query_last_acquisition_of(
            sensor_id=api_param.sensor_id,
            ch_name=api_param.ch_name
        )

    def _urls_of(self, api_param: APIParam) -> AtmotubeTimeIterableURL:
        pre_formatted_url = self._cached_url_template.format(
            api_key=api_param.api_key,
            api_id=api_param.api_id,
            api_fmt="json"
        )
        return AtmotubeTimeIterableURL(
            url=pre_formatted_url,
            begin=api_param.last_acquisition,
            step_size_in_days=1
        )

    def _rotate_file(self, sensor_id: int):
        sensor_ident = self._database_gway.query_mobile_sensor_unique_info(sensor_id=sensor_id)
        _FILE_ROTATOR.rotate(sensor_ident=sensor_ident)

# =========== RUN METHOD
    def run(self):
        for param in self._api_param:
            self._rotate_file(sensor_id=param.sensor_id)
            _LOGGER.info(constants.START_MESSAGE)
            _LOGGER.debug("parameters in use for fetching sensor data => %s" % repr(param))
            for url in self._urls_of(param):
                _LOGGER.debug("downloading sensor measures at => %s" % url)

                server_jresp = json_http_response(url=url)
                _LOGGER.debug("successfully get server response!!!")

                datamodel_builder = AtmotubeAPIDataBuilder(json_response=server_jresp)
                _LOGGER.debug("found #%d API data" % len(datamodel_builder))

                request_builder = AddAtmotubeMeasureRequestBuilder(
                    datamodel=datamodel_builder,
                    timest=_TIMEST,
                    code2id=self._measure_param
                )
                _LOGGER.debug("found #%d requests" % len(request_builder))

                validator = AddSensorMeasuresRequestValidator(
                    request=request_builder,
                    filter_ts=self._filter_ts_of(param)
                )
                _LOGGER.debug('found #%d valid requests' % len(validator))

                response_builder = AddMobileMeasureResponseBuilder(
                    requests=validator,
                    start_packet_id=self._packet_id()
                )
                _LOGGER.debug("found #%d responses" % len(response_builder))

                if len(response_builder) > 0:
                    _LOGGER.debug("responses time range: [%s - %s]" % (validator[0].timestamp, validator[-1].timestamp))
                    query = _build_insert_query(response_builder)
                    query += _build_update_query(
                        time=validator[-1].timestamp,
                        sensor_id=param.sensor_id,
                        channel_name=param.ch_name
                    )
                    self._database_gway.execute(query=query)
            _LOGGER.info(constants.END_MESSAGE)
