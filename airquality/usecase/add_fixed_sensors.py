######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 20:55
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Set
from airquality.database.gateway import DatabaseGateway
from airquality.apidata_builder import PurpleairAPIDataBuilder
from airquality.request_builder import AddPurpleairSensorRequestBuilder
from airquality.request_validator import AddFixedSensorRequestValidator
from airquality.response_builder import AddFixedSensorResponseBuilder


class AddFixedSensors(object):
    """
    An *object* that represent the UseCase of adding new fixed sensors (i.e., a station) to the database.
    """

    def __init__(
            self,
            output_gateway: DatabaseGateway,            # The database output boundary.
            existing_names: Set[str],                   # The set of names already present into the database.
            start_sensor_id: int                        # The id from where to start insert all the sensors.
    ):
        self.output_gateway = output_gateway
        self.existing_names = existing_names
        self.start_sensor_id = start_sensor_id

    def process(self, datamodels: PurpleairAPIDataBuilder):
        print(f"found #{len(datamodels)} datamodels")
        requests = AddPurpleairSensorRequestBuilder(datamodel=datamodels)
        print(f"found #{len(requests)} requests")
        validated_requests = AddFixedSensorRequestValidator(request=requests, existing_names=self.existing_names)
        print(f"found #{len(validated_requests)} valid requests")
        responses = AddFixedSensorResponseBuilder(requests=validated_requests, start_sensor_id=self.start_sensor_id)
        if responses:
            print(f"found #{len(responses)} responses")
            self.output_gateway.insert_sensors(responses=responses)
