######################################################
#
# Author: Davide Colombo
# Date: 01/01/22 16:53
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.core.request_validator import AddSensorMeasuresRequestValidator
from airquality.core.response_builder import AddStationMeasuresResponseBuilder
from airquality.database.gateway import DatabaseGateway
from airquality.datamodel.apiparam import APIParam
from datetime import datetime


class AddStationMeasures(object):
    """
    An *object* that represents the UseCase of adding station measurements to the database
    through the *output_gateway*.
    """

    def __init__(
            self,
            output_gateway: DatabaseGateway,            # The database output boundary.
            filter_ts: datetime,                        # The timestamp used to validate the requests.
            start_packet_id: int,                       # The id from where to start inserting all the packets.
            apiparam: APIParam
    ):
        self.output_gateway = output_gateway
        self.filter_ts = filter_ts
        self.start_packet_id = start_packet_id
        self.apiparam = apiparam

    def process(self, requests):
        print(f"found #{len(requests)} requests")
        valid_requests = AddSensorMeasuresRequestValidator(request=requests, filter_ts=self.filter_ts)
        print(f"found #{len(valid_requests)} valid requests")
        responses = AddStationMeasuresResponseBuilder(
            requests=valid_requests, start_packet_id=self.start_packet_id, sensor_id=self.apiparam.sensor_id
        )
        if responses:
            print(f"found responses within [{valid_requests[0].timestamp!s} - {valid_requests[-1].timestamp!s}]")
            self.output_gateway.insert_station_measures(responses=responses)
            last_acquisition = valid_requests[-1].timestamp.strftime("%Y-%m-%d %H:%M:%S")
            self.output_gateway.update_last_acquisition(
                timestamp=last_acquisition, sensor_id=self.apiparam.sensor_id, ch_name=self.apiparam.ch_name
            )
