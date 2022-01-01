######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 11:54
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict
from datetime import datetime
from airquality.database.gateway import DatabaseGateway
from airquality.core.apidata_builder import AtmotubeAPIDataBuilder
from airquality.core.request_builder import AddAtmotubeMeasureRequestBuilder
from airquality.core.request_validator import AddSensorMeasuresRequestValidator
from airquality.core.response_builder import AddMobileMeasureResponseBuilder


class AddMobileMeasures(object):
    """
    An *object* that represents the UseCase of adding mobile measurements to the database
    through the *output_gateway
    """

    def __init__(
            self,
            output_gateway: DatabaseGateway,            # The database output boundary.
            code2id: Dict[str, int],                    # The map between measure param code and id.
            filter_ts: datetime,                        # The timestamp used to validate the requests.
            start_packet_id: int,                       # The id from where to start inserting all the packets.
            sensor_id: int,                             # The unique id of the sensor that collects the measurements.
            ch_name: str                                # The sensor's acquisition channel name.
    ):
        self.output_gateway = output_gateway
        self.code2id = code2id
        self.filter_ts = filter_ts
        self.start_packet_id = start_packet_id
        self.sensor_id = sensor_id
        self.ch_name = ch_name

    def process(self, datamodels: AtmotubeAPIDataBuilder):
        print(f"found #{len(datamodels)} datamodels")
        requests = AddAtmotubeMeasureRequestBuilder(datamodel=datamodels, code2id=self.code2id)
        print(f"found #{len(requests)} requests")
        valid_requests = AddSensorMeasuresRequestValidator(request=requests, filter_ts=self.filter_ts)
        print(f"found #{len(valid_requests)} valid requests")
        responses = AddMobileMeasureResponseBuilder(requests=valid_requests, start_packet_id=self.start_packet_id)

        if responses:
            print(f"found responses within [{valid_requests[0].timestamp!s} - {valid_requests[-1].timestamp!s}]")
            self.output_gateway.insert_mobile_sensor_measures(responses=responses)
            last_acquisition = valid_requests[-1].timestamp.strftime("%Y-%m-%d %H:%M:%S")
            self.output_gateway.update_last_acquisition(timestamp=last_acquisition, sensor_id=self.sensor_id, ch_name=self.ch_name)
