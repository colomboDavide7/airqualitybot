######################################################
#
# Author: Davide Colombo
# Date: 01/01/22 16:53
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import logging
from datetime import datetime
import airquality.environment as environ
import airquality.usecase as constants
from airquality.usecase.abc import UsecaseABC
from airquality.extra.timest import thingspeak_timest
from airquality.datamodel.apiparam import APIParam
from airquality.database.gateway import DatabaseGateway
from airquality.url.url_reader import json_http_response
from airquality.extra.logger_extra import FileHandlerRotator
from airquality.url.timeiter_url import ThingspeakTimeIterableURL
from airquality.core.apidata_builder import ThingspeakAPIDataBuilder
from airquality.core.request_builder import AddThingspeakMeasuresRequestBuilder
from airquality.core.request_validator import AddSensorMeasuresRequestValidator
from airquality.core.response_builder import AddStationMeasuresResponseBuilder


_ENVIRON = environ.get_environ()
_LOGGER = logging.getLogger(__name__)
_FILE_ROTATOR = FileHandlerRotator(
    logger_name=_LOGGER.name,
    logger_level=_LOGGER.level,
    logger_dir=_ENVIRON.logging_dir_of(personality='thingspeak')
)
_TIMEST = thingspeak_timest()

MAPPING_1A = {'field1': 'pm1.0_atm_a', 'field2': 'pm2.5_atm_a', 'field3': 'pm10.0_atm_a', 'field6': 'temperature_a',
              'field7': 'humidity_a'}
MAPPING_1B = {'field1': 'pm1.0_atm_b', 'field2': 'pm2.5_atm_b', 'field3': 'pm10.0_atm_b', 'field6': 'pressure_b'}
MAPPING_2A = {'field1': '0.3_um_count_a', 'field2': '0.5_um_count_a', 'field3': '1.0_um_count_a',
              'field4': '2.5_um_count_a', 'field5': '5.0_um_count_a', 'field6': '10.0_um_count_a'}
MAPPING_2B = {'field1': '0.3_um_count_b', 'field2': '0.5_um_count_b', 'field3': '1.0_um_count_b',
              'field4': '2.5_um_count_b', 'field5': '5.0_um_count_b', 'field6': '10.0_um_count_b'}
FIELD_MAP = {'1A': MAPPING_1A, '1B': MAPPING_1B, '2A': MAPPING_2A, '2B': MAPPING_2B}


def _fields_of(param: APIParam):
    return FIELD_MAP[param.ch_name]


def _build_update_query(time: datetime, sensor_id: int, channel_name: str) -> str:
    return "UPDATE level0_raw.sensor_api_param " \
           f"SET last_acquisition = '{time}' " \
           f"WHERE sensor_id = {sensor_id} AND ch_name = '{channel_name}';"


def _build_insert_query(response_builder: AddStationMeasuresResponseBuilder) -> str:
    return "INSERT INTO level0_raw.station_measurement " \
           "(packet_id, sensor_id, param_id, param_value, timestamp) " \
           f"VALUES {','.join(resp.measure_record for resp in response_builder)};"


class AddPurpleairMeasures(UsecaseABC):
    def __init__(self, database_gway: DatabaseGateway):
        self._database_gway = database_gway
        self._measure_param = self._database_gway.query_measure_param_owned_by(owner="thingspeak")
        self._api_param = self._database_gway.query_sensor_apiparam_of_type(sensor_type="thingspeak")
        self._url_template = _ENVIRON.url_template(personality='thingspeak')

    def _packet_id(self) -> int:
        return self._database_gway.query_max_station_packet_id_plus_one()

    def _filter_ts_of(self, param: APIParam) -> datetime:
        return self._database_gway.query_last_acquisition_of(
            sensor_id=param.sensor_id,
            ch_name=param.ch_name
        )

    def _urls_of(self, param: APIParam) -> ThingspeakTimeIterableURL:
        pre_formatted_url = self._url_template.format(
            api_key=param.api_key,
            api_id=param.api_id,
            api_fmt="json"
        )
        return ThingspeakTimeIterableURL(
            url=pre_formatted_url,
            begin=param.last_acquisition,
            step_size_in_days=7
        )

    def _rotate_file(self, sensor_id: int):
        sensor_ident = self._database_gway.query_fixed_sensor_unique_info(sensor_id=sensor_id)
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
                _LOGGER.debug("successfully get server response")

                datamodel_builder = ThingspeakAPIDataBuilder(json_response=server_jresp)
                _LOGGER.debug("found #%d API data" % len(datamodel_builder))

                request_builder = AddThingspeakMeasuresRequestBuilder(
                    datamodel=datamodel_builder,
                    timest=_TIMEST,
                    code2id=self._measure_param,
                    field_map=_fields_of(param)
                )
                _LOGGER.debug("found #%d requests" % len(request_builder))

                validator = AddSensorMeasuresRequestValidator(
                    request=request_builder,
                    filter_ts=self._filter_ts_of(param)
                )
                _LOGGER.debug('found #%d valid responses' % len(validator))

                response_builder = AddStationMeasuresResponseBuilder(
                    requests=validator,
                    start_packet_id=self._packet_id(),
                    sensor_id=param.sensor_id
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
