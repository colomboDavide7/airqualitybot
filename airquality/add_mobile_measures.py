######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 11:54
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict
from datetime import datetime
from airquality.database_gateway import DatabaseGateway
from airquality.datamodel_builder import AtmotubeDatamodelBuilder
from airquality.request_builder import AddAtmotubeMeasureRequestBuilder
from airquality.request_validator import AddMobileMeasureRequestValidator
from airquality.response_builder import AddMobileMeasureResponseBuilder


class AddMobileMeasures(object):

    def __init__(
            self,
            output_gateway: DatabaseGateway,
            code2id: Dict[str, int],
            filter_ts: datetime,
            start_packet_id: int,
            sensor_id: int,
            ch_name: str
    ):
        self.output_gateway = output_gateway
        self.code2id = code2id
        self.filter_ts = filter_ts
        self.start_packet_id = start_packet_id
        self.sensor_id = sensor_id
        self.ch_name = ch_name

    def process(self, datamodels: AtmotubeDatamodelBuilder):
        requests = AddAtmotubeMeasureRequestBuilder(datamodel=datamodels, code2id=self.code2id)
        valid_requests = AddMobileMeasureRequestValidator(request=requests, filter_ts=self.filter_ts)
        responses = AddMobileMeasureResponseBuilder(requests=valid_requests, start_packet_id=self.start_packet_id)
        self.output_gateway.insert_mobile_sensor_measures(responses=responses)
        last_acquisition = valid_requests[-1].timestamp.strftime("%Y-%m-%d %H:%M:%S")
        self.output_gateway.update_last_acquisition(timestamp=last_acquisition, sensor_id=self.sensor_id, ch_name=self.ch_name)
