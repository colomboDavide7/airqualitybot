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
import math
from datetime import datetime
import airquality.usecase as constants
from airquality.usecase.abc import UsecaseABC
from airquality.datamodel.geometry import PostgisPoint
from airquality.database.gateway import DatabaseGateway
from airquality.url.url_reader import json_http_response
from airquality.datamodel.fromapi import PurpleairDM
from airquality.iterables.fromapi import PurpleairIterableDatamodels


def _build_query(sensor_id: int, time: datetime, geom: str):
    return f"UPDATE level0_raw.sensor_at_location SET valid_to = '{time}' " \
           f"WHERE sensor_id = {sensor_id} AND valid_to IS NULL;" \
           "INSERT INTO level0_raw.sensor_at_location (sensor_id, valid_from, geom) " \
           f"VALUES ({sensor_id}, '{time}', {geom});"


class UpdatePurpleairLocation(UsecaseABC):
    def __init__(self, database_gway: DatabaseGateway):
        self._database_gway = database_gway
        self._url_template = _ENVIRON.url_template(personality='purp_update')

    def _safe_query_location_of(self, datamodel: PurpleairDM):
        try:
            geo = self._database_gway.query_purpleair_location_of(sensor_index=datamodel.sensor_index)
            if not math.isclose(a=datamodel.latitude, b=geo.latitude, rel_tol=1e-5) or \
               not math.isclose(a=datamodel.longitude, b=geo.longitude, rel_tol=1e-5):
                _LOGGER.debug("update sensor_id = '%d'" % geo.sensor_id)
                _LOGGER.debug("set location to => (%.6f, %.6f)" % (datamodel.longitude, datamodel.latitude))

                geom = str(PostgisPoint(latitude=datamodel.latitude, longitude=datamodel.longitude))
                query = _build_query(sensor_id=geo.sensor_id, time=_TIMEST.current_utc_timetz(), geom=geom)
                self._database_gway.execute(query=query)

        except ValueError:
            _LOGGER.warning("Cannot found 'open' location (valid_to = NULL) corresponding to sensor '%s' "
                            "(sensor_index = %d) in level0_raw.sensor_at_location table" %
                            (datamodel.name, datamodel.sensor_index))

    def run(self):
        _LOGGER.info(constants.START_MESSAGE)

        server_jresp = json_http_response(url=self._url_template)
        _LOGGER.debug("successfully get server response!!!")

        datamodel_builder = PurpleairIterableDatamodels(json_response=server_jresp)
        _LOGGER.debug("found #%d API items" % len(datamodel_builder))

        for datamodel in datamodel_builder:
            self._safe_query_location_of(datamodel=datamodel)

        _LOGGER.info(constants.END_MESSAGE)

    def __repr__(self):
        return f"{type(self).__name__}"
