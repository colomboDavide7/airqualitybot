# ======================================
# @author:  Davide Colombo
# @date:    2022-01-27, gio, 16:51
# ======================================
import logging
from airquality.extra.decorators import catch
import airquality.usecase as constants
import airquality.environment as environ
from airquality.url.url_reader import json_http_response
from airquality.database.gateway import DatabaseGateway
from airquality.datamodel.geolocation import Geolocation
from airquality.datamodel.apidata import PurpleairLocationData
from airquality.core.apidata_builder import PurpleairAPIDataBuilder

_LOGGER = logging.getLogger(__name__)
_ENVIRON = environ.get_environ()


class UpdatePurpleairLocation(object):

    def __init__(self, database_gway: DatabaseGateway):
        self._database_gway = database_gway
        self._url_template = _ENVIRON.url_template(personality='purp_update')

    @catch(exc_type=ValueError, logger_name=__name__)
    def _safe_query_location(self, sensor_index: int) -> Geolocation:
        return self._database_gway.query_purpleair_location(sensor_index=sensor_index)

    def run(self):
        _LOGGER.info(constants.START_MESSAGE)

        server_jresp = json_http_response(url=self._url_template)
        _LOGGER.debug("successfully get server response!!!")

        datamodel_builder = PurpleairAPIDataBuilder(
            json_response=server_jresp,
            item_fact=PurpleairLocationData
        )
        _LOGGER.debug("found #%d API data" % len(datamodel_builder))

        for datamodel in datamodel_builder:
            db_geo = self._safe_query_location(sensor_index=datamodel.sensor_index)
            print(repr(db_geo))

        _LOGGER.info(constants.END_MESSAGE)

    def __repr__(self):
        return f"{type(self).__name__}"
