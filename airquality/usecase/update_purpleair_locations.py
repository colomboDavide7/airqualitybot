# ======================================
# @author:  Davide Colombo
# @date:    2022-01-27, gio, 16:51
# ======================================
import logging
import airquality.environment as environ
from airquality.extra.timest import Timest

_LOGGER = logging.getLogger(__name__)
_ENVIRON = environ.get_environ()
_TIMEST = Timest()

# ======================================
from datetime import datetime
import airquality.usecase as constants
from airquality.datamodel.geometry import PostgisPoint
from airquality.usecase.abc import UsecaseABC
from airquality.url.url_reader import json_http_response
from airquality.database.gateway import DatabaseGateway
from airquality.datamodel.apidata import PurpleairLocationData
from airquality.core.apidata_builder import PurpleairAPIDataBuilder


def _build_insert_query(sensor_id: int, valid_from: datetime, geom: str):
    return "INSERT INTO level0_raw.sensor_at_location (sensor_id, valid_from, geom) " \
           f"VALUES ({sensor_id}, '{valid_from}', {geom});"


class UpdatePurpleairLocation(UsecaseABC):
    def __init__(self, database_gway: DatabaseGateway):
        self._database_gway = database_gway
        self._url_template = _ENVIRON.url_template(personality='purp_update')

    def run(self):
        _LOGGER.info(constants.START_MESSAGE)

        server_jresp = json_http_response(url=self._url_template)
        _LOGGER.debug("successfully get server response!!!")

        datamodel_builder = PurpleairAPIDataBuilder(
            json_response=server_jresp,
            item_fact=PurpleairLocationData
        )
        _LOGGER.debug("found #%d API items" % len(datamodel_builder))

        # for datamodel in datamodel_builder:
        #     try:
        #         db_geo = self._database_gway.query_purpleair_location(sensor_index=datamodel.sensor_index)
        #         print(repr(db_geo))
        #     except ValueError:
        #         _LOGGER.debug("Cannot found a Purpleair sensor with index = '{sensor_index}'")
        #
        #         # TODO: query sensor_id from sensor_index
        #
        #         geometry = PostgisPoint(latitude=datamodel.latitude, longitude=datamodel.longitude)
        #         query = _build_insert_query(
        #             sensor_id=,
        #             valid_from=_TIMEST.current_utc_timetz(),
        #             geom=geometry.geom_from_text()
        #         )
        #         self._database_gway.execute(query=query)

        _LOGGER.info(constants.END_MESSAGE)

    def __repr__(self):
        return f"{type(self).__name__}"
