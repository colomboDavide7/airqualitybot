# ======================================
# @author:  Davide Colombo
# @date:    2022-01-27, gio, 16:51
# ======================================
import logging
from airquality.extra.decorators import catch
import airquality.usecase as constants
from airquality.environment import get_environ
from airquality.url.url_reader import URLReader
from airquality.database.gateway import DatabaseGateway
from airquality.datamodel.geolocation import Geolocation
from airquality.datamodel.apidata import PurpleairLocationData
from airquality.core.apidata_builder import PurpleairAPIDataBuilder


class UpdatePurpleairLocation(object):

    def __init__(
        self,
        database_gway: DatabaseGateway,
        url_reader: URLReader
    ):
        self._url_reader = url_reader
        self._database_gway = database_gway
        self._environ = get_environ()
        self._logger = logging.getLogger(__name__)

    def _url(self) -> str:
        return self._environ.url_template(personality='purp_update')

    @catch(exc_type=ValueError, logger_name=__name__)
    def _safe_query_location(self, sensor_index: int) -> Geolocation:
        return self._database_gway.query_purpleair_location(sensor_index=sensor_index)

    def run(self):
        self._logger.info(constants.START_MESSAGE)

        server_jresp = self._url_reader.json(url=self._url())
        self._logger.debug("successfully get server response!!!")

        datamodel_builder = PurpleairAPIDataBuilder(
            json_response=server_jresp,
            item_fact=PurpleairLocationData
        )
        self._logger.debug("found #%d API data" % len(datamodel_builder))

        for datamodel in datamodel_builder:
            db_geo = self._safe_query_location(sensor_index=datamodel.sensor_index)
            print(repr(db_geo))

        self._logger.info(constants.END_MESSAGE)

    def __repr__(self):
        return f"{type(self).__name__}"
