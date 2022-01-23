######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 20:55
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import logging
import airquality.environment as environ
from airquality.datamodel.timest import Timest
from airquality.database.gateway import DatabaseGateway
from airquality.url.api_server_wrap import APIServerWrapper
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

    def __init__(
        self,
        database_gway: DatabaseGateway,
        server_wrap: APIServerWrapper,
        timest: Timest
    ):
        self._timest = timest
        self._server_wrap = server_wrap
        self._database_gway = database_gway
        self._environ = environ.get_environ()
        self._logger = logging.getLogger(__name__)

    @property
    def start_sensor_id(self) -> int:
        return self._database_gway.query_max_sensor_id_plus_one()

    @property
    def names_of(self):
        return self._database_gway.query_sensor_names_of_type(sensor_type='purpleair')

    def _url_template(self) -> str:
        return self._environ.url_template(
            personality='purpleair'
        )

    def run(self) -> None:
        self._logger.debug("fetching purpleair data at => %s" % self._url_template())

        server_jresp = self._server_wrap.json(url=self._url_template())
        self._logger.debug("successfully get server response!!!")

        datamodel_builder = PurpleairAPIDataBuilder(json_response=server_jresp)
        self._logger.debug("found #%d API data" % len(datamodel_builder))

        request_builder = AddPurpleairSensorRequestBuilder(datamodel=datamodel_builder, timest=self._timest)
        self._logger.debug("found #%d requests" % len(request_builder))

        validator = AddFixedSensorRequestValidator(request=request_builder, existing_names=self.names_of)
        self._logger.debug("found #%d valid requests" % len(validator))

        response_builder = AddFixedSensorResponseBuilder(requests=validator, start_sensor_id=self.start_sensor_id)
        self._logger.debug("found #%d responses" % len(response_builder))

        if response_builder:
            self._logger.debug("inserting new sensors!")
            self._database_gway.insert_sensors(responses=response_builder)
