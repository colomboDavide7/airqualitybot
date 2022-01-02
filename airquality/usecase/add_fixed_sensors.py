######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 20:55
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.database.gateway import DatabaseGateway
from airquality.core.apidata_builder import PurpleairAPIDataBuilder
from airquality.core.request_builder import AddPurpleairSensorRequestBuilder
from airquality.core.request_validator import AddFixedSensorRequestValidator
from airquality.core.response_builder import AddFixedSensorResponseBuilder


class AddPurpleairFixedSensors(object):
    """
    An *object* that defines the UseCase of adding Purpleair sensors.

    The sensor information are fetched from the Purpleair API.
    Only the sensors that are not present into the database at the moment the application is run are inserted.
    The goal of this class is to transform a set of Purpleair API data into valid SQL for inserting them.
    """

    def __init__(self, output_gateway: DatabaseGateway, input_url_template: str):
        self.output_gateway = output_gateway
        self.input_url_template = input_url_template

    @property
    def start_sensor_id(self) -> int:
        return self.output_gateway.get_max_sensor_id_plus_one()

    @property
    def names_of(self):
        return self.output_gateway.get_existing_sensor_names_of_type(sensor_type='purpleair')

    def run(self) -> None:
        datamodel_builder = PurpleairAPIDataBuilder(url=self.input_url_template)
        print(f"found #{len(datamodel_builder)} API data")

        request_builder = AddPurpleairSensorRequestBuilder(datamodel=datamodel_builder)
        print(f"found #{len(request_builder)} requests")

        validator = AddFixedSensorRequestValidator(request=request_builder, existing_names=self.names_of)
        print(f"found #{len(validator)} valid requests")

        responses = AddFixedSensorResponseBuilder(requests=validator, start_sensor_id=self.start_sensor_id)
        print(f"found #{len(responses)} responses")

        if len(responses) > 0:
            print(f"insert new sensors!")
            self.output_gateway.insert_sensors(responses=responses)
