######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 20:55
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import logging
import airquality.environment as environ

_LOGGER = logging.getLogger(__name__)
_ENVIRON = environ.get_environ()

######################################################
import airquality.usecase as constant
from airquality.usecase.abc import UsecaseABC
from airquality.extra.url import json_http_response
from airquality.extra.decorator import log_context
from airquality.database.gateway import DatabaseGateway
from airquality.iterables.fromapi import PurpleairIterableDatamodels
from airquality.iterables.requests import PurpleairIterableRequests
from airquality.iterables.validator import FixedSensorIterableValidRequests
from airquality.iterables.responses import FixedSensorIterableResponses


class Purpleair(UsecaseABC):
    """
    A class that implements the *UsecaseABC* interface and defines the business rules for inserting purpleair
    sensor records downloaded from the API
    """

    def __init__(self, database_gway: DatabaseGateway):
        self._database_gway = database_gway
        self._url_template = _ENVIRON.url_template(personality='purpleair')
        self._start_sensor_id = self._database_gway.query_max_sensor_id_plus_one()
        self._database_sensor_names = self._database_gway.query_sensor_names_of_type(sensor_type='purpleair')

    @log_context(logger_name=__name__, header=constant.START_MESSAGE, teardown=constant.END_MESSAGE)
    def execute(self):
        server_jresp = json_http_response(url=self._url_template)
        datamodels = PurpleairIterableDatamodels(json_response=server_jresp)
        requests = PurpleairIterableRequests(datamodels=datamodels)
        valid_requests = FixedSensorIterableValidRequests(request=requests, name2remove=self._database_sensor_names)
        if not valid_requests:
            _LOGGER.debug('all the sensors are already stored into the database')
            return

        responses = FixedSensorIterableResponses(requests=valid_requests, start_sensor_id=self._start_sensor_id)
        self._database_gway.execute(responses.query())
        _LOGGER.debug("inserted %d/%d sensors" % (len(valid_requests), len(datamodels)))
