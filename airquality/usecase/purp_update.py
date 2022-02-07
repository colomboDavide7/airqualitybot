# ======================================
# @author:  Davide Colombo
# @date:    2022-01-27, gio, 16:51
# ======================================
import logging
import airquality.environment as environ

_LOGGER = logging.getLogger(__name__)
_ENVIRON = environ.get_environ()

# ======================================
import math
from datetime import datetime
import airquality.usecase as constants
import airquality.extra.timest as timest
from airquality.usecase.abc import UsecaseABC
from airquality.extra.decorator import log_context
from airquality.datamodel.geometry import PostgisPoint
from airquality.database.gateway import DatabaseGateway
from airquality.extra.url import json_http_response
from airquality.datamodel.fromapi import PurpleairDM
from airquality.iterables.fromapi import PurpleairIterableDatamodels


def _build_query(sensor_id: int, time: datetime, geom: PostgisPoint):
    return f"UPDATE level0_raw.sensor_at_location SET valid_to = '{time}' " \
           f"WHERE sensor_id = {sensor_id} AND valid_to IS NULL;" \
           "INSERT INTO level0_raw.sensor_at_location (sensor_id, valid_from, geom) " \
           f"VALUES ({sensor_id}, '{time}', {geom});"


def _has_changed_location(datamodel: PurpleairDM, geo) -> bool:
    """
    A function that returns true if either datamodel's latitude or longitude is changed in respect to geo (i.e.,
    the database location of the sensor)
    """

    return not math.isclose(a=datamodel.latitude, b=geo.latitude, rel_tol=1e-5) or \
           not math.isclose(a=datamodel.longitude, b=geo.longitude, rel_tol=1e-5)


class PurpUpdate(UsecaseABC):
    def __init__(self, database_gway: DatabaseGateway):
        self._database_gway = database_gway
        self._url_template = _ENVIRON.url_template(personality='purp_update')

    def _safe_query_location_of(self, datamodel: PurpleairDM):
        try:
            geo = self._database_gway.query_purpleair_sensor_location(sensor_index=datamodel.sensor_index)
            if _has_changed_location(datamodel=datamodel, geo=geo):
                geom = PostgisPoint(latitude=datamodel.latitude, longitude=datamodel.longitude)
                query = _build_query(sensor_id=geo.sensor_id, time=timest.now_utctz(), geom=geom)
                self._database_gway.execute(query=query)
                _LOGGER.debug("Update sensor at id = '%d' set location to => (%.6f, %.6f)" %
                              (geo.sensor_id, datamodel.longitude, datamodel.latitude))
        except ValueError as err:
            _LOGGER.warning(str(err))

    @log_context(logger_name=__name__, header=constants.START_MESSAGE, teardown=constants.END_MESSAGE)
    def execute(self):
        server_jresp = json_http_response(url=self._url_template)
        datamodels = PurpleairIterableDatamodels(json_response=server_jresp)
        for datamodel in datamodels:
            self._safe_query_location_of(datamodel=datamodel)
