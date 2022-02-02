######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 20:55
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import logging
import airquality.environment as environ
from airquality.extra.timest import purpleair_timest

_LOGGER = logging.getLogger(__name__)
_ENVIRON = environ.get_environ()
_TIMEST = purpleair_timest()

######################################################
import airquality.usecase as constant
from airquality.usecase.abc import UsecaseABC
from airquality.database.gateway import DatabaseGateway
from airquality.url.url_reader import json_http_response
from airquality.iterables.fromapi import PurpleairIterableDatamodels
from airquality.iterables.request_builder import AddPurpleairSensorRequestBuilder
from airquality.iterables.request_validator import AddFixedSensorRequestValidator
from airquality.iterables.response_builder import AddFixedSensorResponseBuilder


def _build_insert_query(response_builder: AddFixedSensorResponseBuilder) -> str:
    sval = pval = ""
    for r in response_builder:
        sval += f"{r.sensor_record},"
        pval += f"{r.apiparam_record},"
    query = f"INSERT INTO level0_raw.sensor VALUES {sval.strip(',')};"
    query += "INSERT INTO level0_raw.sensor_api_param " \
             "(sensor_id, ch_key, ch_id, ch_name, last_acquisition) " \
             f"VALUES {pval.strip(',')};"
    return query


class AddPurpleairFixedSensors(UsecaseABC):
    def __init__(self, database_gway: DatabaseGateway):
        self._database_gway = database_gway
        self._url_template = _ENVIRON.url_template(personality='purpleair')
        self._start_sensor_id = self._database_gway.query_max_sensor_id_plus_one()
        self._database_sensor_names = self._database_gway.query_sensor_names_of_type(sensor_type='purpleair')

    def run(self):
        _LOGGER.info(constant.START_MESSAGE)
        _LOGGER.debug("fetching purpleair data at => %s" % self._url_template)

        server_jresp = json_http_response(url=self._url_template)
        _LOGGER.debug("successfully get server response!!!")

        datamodel_builder = PurpleairIterableDatamodels(json_response=server_jresp)
        _LOGGER.debug("found #%d API data" % len(datamodel_builder))

        request_builder = AddPurpleairSensorRequestBuilder(
            datamodel=datamodel_builder,
            timest=_TIMEST
        )
        _LOGGER.debug("found #%d requests" % len(request_builder))

        validator = AddFixedSensorRequestValidator(
            request=request_builder,
            existing_names=self._database_sensor_names
        )
        _LOGGER.debug("found #%d valid requests" % len(validator))

        response_builder = AddFixedSensorResponseBuilder(
            requests=validator,
            start_sensor_id=self._start_sensor_id
        )
        _LOGGER.debug("found #%d responses" % len(response_builder))

        if len(response_builder) > 0:
            _LOGGER.debug("inserting new sensors!")
            query = _build_insert_query(response_builder)
            self._database_gway.execute(query)
        _LOGGER.info(constant.END_MESSAGE)
