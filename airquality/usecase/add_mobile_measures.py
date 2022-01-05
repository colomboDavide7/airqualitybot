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
from airquality.datamodel.apiparam import APIParam
from airquality.database.gateway import DatabaseGateway
from airquality.url.timeiter_url import AtmotubeTimeIterableURL
from airquality.core.apidata_builder import AtmotubeAPIDataBuilder
from airquality.core.request_builder import AddAtmotubeMeasureRequestBuilder
from airquality.core.request_validator import AddSensorMeasuresRequestValidator
from airquality.core.response_builder import AddMobileMeasureResponseBuilder


class AddAtmotubeMeasures(object):
    """
    A *UsecaseRunner* that defines how to run the *AddMobileMeasures* UseCase.
    """

    def __init__(self, output_gateway: DatabaseGateway, input_url_template: str):
        self.output_gateway = output_gateway
        self.input_url_template = input_url_template
        self.app_logger = logging.getLogger(__name__)

    @property
    def measure_param(self) -> Dict[str, int]:
        return self.output_gateway.get_measure_param_owned_by(owner="atmotube")

    @property
    def api_param(self) -> List[APIParam]:
        return self.output_gateway.get_apiparam_of_type(sensor_type="atmotube")

    @property
    def start_packet_id(self) -> int:
        return self.output_gateway.get_max_mobile_packet_id_plus_one()

    def filter_ts_of(self, param: APIParam) -> datetime:
        return self.output_gateway.get_last_acquisition_of_sensor_channel(sensor_id=param.sensor_id, ch_name=param.ch_name)

    def urls_of(self, param: APIParam) -> AtmotubeTimeIterableURL:
        pre_formatted_url = self.input_url_template.format(api_key=param.api_key, api_id=param.api_id, api_fmt="json")
        return AtmotubeTimeIterableURL(url=pre_formatted_url, begin=param.last_acquisition, step_size_in_days=1)

    def run(self):
        measure_param = self.measure_param
        for param in self.api_param:
            self.app_logger.info("sensor => %s" % repr(param))
            for url in self.urls_of(param):
                self.app_logger.info("url => %s" % url)
                datamodel_builder = AtmotubeAPIDataBuilder(url=url)
                self.app_logger.info("found #%d API data" % len(datamodel_builder))

                request_builder = AddAtmotubeMeasureRequestBuilder(datamodel=datamodel_builder, code2id=measure_param)
                self.app_logger.info("found #%d requests" % len(request_builder))

                validator = AddSensorMeasuresRequestValidator(request=request_builder, filter_ts=self.filter_ts_of(param))
                self.app_logger.info("found #%d valid requests" % len(validator))

                response_builder = AddMobileMeasureResponseBuilder(requests=validator, start_packet_id=self.start_packet_id)
                self.app_logger.info("found #%d responses" % len(response_builder))

                if response_builder:
                    self.app_logger.info("found responses within: [%s - %s]" % (validator[0].timestamp, validator[-1].timestamp))
                    self.output_gateway.insert_mobile_sensor_measures(responses=response_builder)
                    last_acquisition = validator[-1].timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    self.output_gateway.update_last_acquisition(
                        timestamp=last_acquisition, sensor_id=param.sensor_id, ch_name=param.ch_name
                    )
