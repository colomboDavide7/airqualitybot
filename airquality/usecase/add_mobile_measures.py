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
from airquality.datamodel.timest import Timest
from airquality.datamodel.apiparam import APIParam
from airquality.database.gateway import DatabaseGateway
from airquality.url.api_server_wrap import APIServerWrapper
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
            self, database_gway: DatabaseGateway, server_wrap: APIServerWrapper, timest: Timest, input_url_template: str
    ):
        self._timest = timest
        self._database_gway = database_gway
        self._server_wrap = server_wrap
        self.input_url_template = input_url_template
        self._logger = logging.getLogger(__name__)

    @property
    def measure_param(self) -> Dict[str, int]:
        return self._database_gway.query_measure_param_owned_by(owner="atmotube")

    @property
    def api_param(self) -> List[APIParam]:
        return self._database_gway.get_sensor_apiparam_of_type(sensor_type="atmotube")

    @property
    def start_packet_id(self) -> int:
        return self._database_gway.query_max_mobile_packet_id_plus_one()

    def filter_ts_of(self, param: APIParam) -> datetime:
        return self._database_gway.get_last_acquisition_of(sensor_id=param.sensor_id, ch_name=param.ch_name)

    def urls_of(self, param: APIParam) -> AtmotubeTimeIterableURL:
        pre_formatted_url = self.input_url_template.format(api_key=param.api_key, api_id=param.api_id, api_fmt="json")
        return AtmotubeTimeIterableURL(
            url=pre_formatted_url,
            begin=param.last_acquisition,
            step_size_in_days=1
        )

    def run(self):
        measure_param = self.measure_param
        for param in self.api_param:
            self._logger.info("sensor => %s" % repr(param))
            for url in self.urls_of(param):
                self._logger.info("url => %s" % url)

                server_jresp = self._server_wrap.json(url=url)
                self._logger.debug("successfully get server response!!!")

                datamodel_builder = AtmotubeAPIDataBuilder(json_response=server_jresp)
                self._logger.debug("found #%d API data" % len(datamodel_builder))

                request_builder = AddAtmotubeMeasureRequestBuilder(
                    datamodel=datamodel_builder, timest=self._timest, code2id=measure_param
                )
                self._logger.debug("found #%d requests" % len(request_builder))

                validator = AddSensorMeasuresRequestValidator(
                    request=request_builder, filter_ts=self.filter_ts_of(param)
                )
                self._logger.debug("found #%d valid requests" % len(validator))

                response_builder = AddMobileMeasureResponseBuilder(
                    requests=validator, start_packet_id=self.start_packet_id
                )
                self._logger.debug("found #%d responses" % len(response_builder))

                if response_builder:
                    self._logger.debug(
                        "found responses within: [%s - %s]" % (validator[0].timestamp, validator[-1].timestamp))
                    self._database_gway.insert_mobile_measures(responses=response_builder)
                    last_acquisition = validator[-1].timestamp
                    self._database_gway.update_last_acquisition_of(
                        timestamp=last_acquisition, sensor_id=param.sensor_id, ch_name=param.ch_name
                    )
