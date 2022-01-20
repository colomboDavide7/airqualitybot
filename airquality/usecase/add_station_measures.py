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
from airquality.datamodel.timest import Timest
from airquality.datamodel.apiparam import APIParam
from airquality.database.gateway import DatabaseGateway
from airquality.url.api_server_wrap import APIServerWrapper
from airquality.url.timeiter_url import ThingspeakTimeIterableURL
from airquality.core.apidata_builder import ThingspeakAPIDataBuilder
from airquality.core.request_builder import AddThingspeakMeasuresRequestBuilder
from airquality.core.request_validator import AddSensorMeasuresRequestValidator
from airquality.core.response_builder import AddStationMeasuresResponseBuilder


class AddThingspeakMeasures(object):
    """
    An *object* that defines the application UseCase of adding the measures detected by a fixed sensor (i.e., a station).

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
        self, database_gway: DatabaseGateway, server_wrap: APIServerWrapper, timest: Timest, input_url_template: str
    ):
        self._timest = timest
        self._database_gway = database_gway
        self._server_wrap = server_wrap
        self.input_url_template = input_url_template
        self._logger = logging.getLogger(__name__)

    @property
    def measure_param(self) -> Dict[str, int]:
        return self._database_gway.get_measure_param_owned_by(owner="thingspeak")

    @property
    def api_param(self) -> List[APIParam]:
        return self._database_gway.get_sensor_apiparam_of_type(sensor_type="thingspeak")

    @property
    def start_packet_id(self) -> int:
        return self._database_gway.get_max_station_packet_id_plus_one()

    def fields_of(self, param: APIParam) -> Dict[str, str]:
        return self.FIELD_MAP[param.ch_name]

    def filter_ts_of(self, param: APIParam) -> datetime:
        return self._database_gway.get_last_acquisition_of(sensor_id=param.sensor_id, ch_name=param.ch_name)

    def urls_of(self, param: APIParam) -> ThingspeakTimeIterableURL:
        pre_formatted_url = self.input_url_template.format(api_key=param.api_key, api_id=param.api_id, api_fmt="json")
        return ThingspeakTimeIterableURL(
            url=pre_formatted_url,
            begin=param.last_acquisition,
            step_size_in_days=7
        )

    def run(self) -> None:
        measure_param = self.measure_param
        for param in self.api_param:
            self._logger.info("sensor => %s" % repr(param))
            for url in self.urls_of(param):
                self._logger.info("url => %s" % url)

                server_jresp = self._server_wrap.json(url=url)
                self._logger.debug("successfully get server response!!!")

                datamodel_builder = ThingspeakAPIDataBuilder(json_response=server_jresp)
                self._logger.debug("found #%d API data" % len(datamodel_builder))

                request_builder = AddThingspeakMeasuresRequestBuilder(
                    datamodel=datamodel_builder,
                    timest=self._timest,
                    code2id=measure_param,
                    field_map=self.fields_of(param)
                )
                self._logger.debug("found #%d requests" % len(request_builder))

                validator = AddSensorMeasuresRequestValidator(request=request_builder, filter_ts=self.filter_ts_of(param))
                self._logger.debug("found #%d valid requests" % len(validator))

                response_builder = AddStationMeasuresResponseBuilder(
                    requests=validator, start_packet_id=self.start_packet_id, sensor_id=param.sensor_id
                )
                self._logger.debug("found #%d responses" % len(response_builder))

                if len(response_builder) > 0:
                    self._logger.debug("found responses within: [%s - %s]" % (validator[0].timestamp, validator[-1].timestamp))
                    self._database_gway.insert_station_measures(responses=response_builder)
                    last_acquisition = validator[-1].timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    self._database_gway.update_last_acquisition_of(
                        timestamp=last_acquisition, sensor_id=param.sensor_id, ch_name=param.ch_name
                    )
