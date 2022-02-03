# ======================================
# @author:  Davide Colombo
# @date:    2022-01-23, dom, 12:44
# ======================================

def _custom_log_filename(sensor_id: int, sensor_name: str, sensor_lat: float = None, sensor_lng: float = None) -> str:
    """
    A function that takes a set of sensor parameters and return a custom log filename.
    """

    base_name = f"sensor_{sensor_id}_{string.string_cleaner(s=sensor_name, char2remove=[' ', '.', '-'])}"
    if sensor_lat is None and sensor_lng is None:
        return base_name + '.log'
    return f"{base_name}_{string.literalize_number(sensor_lat)}_{string.literalize_number(sensor_lng)}.log"


# ======================================
import os
import logging
import airquality.extra.string as string
from airquality.datamodel.fromdb import SensorInfoDM

_CUSTOM_LOGGER_FORMAT = '[TIME]: %(asctime)s - [LEVEL]: %(levelname)s - [DESCRIPTION]: %(message)s'


class FileHandlerRotator(object):
    """
    A class that caches the current file handler and defines the business rules for rotating the handler
    when a different sensor is in use.
    """

    def __init__(
        self,
        logger_name: str,                       # the target logger's name for applying handler rotation.
        logger_level,                           # the desired logging level.
        logger_dir="./log",                     # the logging directory path.
        logger_fmt=_CUSTOM_LOGGER_FORMAT        # the desired log record format.
    ):
        self._logger_dir = logger_dir
        self._logger_level = logger_level
        self._logger = logging.getLogger(logger_name)
        self._cached_formatter = logging.Formatter(fmt=logger_fmt)
        self._cached_file_handler = None

    def rotate(self, sensor_ident: SensorInfoDM):
        fname = _custom_log_filename(
            sensor_id=sensor_ident.sensor_id,
            sensor_name=sensor_ident.sensor_name,
            sensor_lat=sensor_ident.sensor_lat,
            sensor_lng=sensor_ident.sensor_lng
        )
        self._attach_handler(filename=fname)

    def _attach_handler(self, filename: str):
        if self._cached_file_handler is not None:
            self._detach_handler()
        fullpath = os.path.join(self._logger_dir, filename)
        self._cached_file_handler = logging.FileHandler(filename=fullpath)
        self._cached_file_handler.setFormatter(fmt=self._cached_formatter)
        self._cached_file_handler.setLevel(level=self._logger_level)
        self._logger.addHandler(self._cached_file_handler)

    def _detach_handler(self):
        self._logger.removeHandler(self._cached_file_handler)
        self._cached_file_handler = None
