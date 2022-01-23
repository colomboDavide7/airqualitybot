# ======================================
# @author:  Davide Colombo
# @date:    2022-01-23, dom, 12:44
# ======================================
import logging
from airquality.datamodel.sensor_ident import SensorIdentity


CHAR_TO_REMOVE = [' ', '.', '-']


def name_cleaner(name: str) -> str:
    """
    A utility function for cleaning names.

    :param name:                the name to clean.
    :return:                    the lowercase input name cleaned from the CHAR_TO_REMOVE chars.
    """

    for c in CHAR_TO_REMOVE:
        if c in name:
            name = name.replace(c, '')
    return name.lower()


def number_cleaner(number: float) -> str:
    """
    A utility function for cleaning number's string representation.

    :param number:              the number to clean.
    :return:                    the string representation of that number with 'dot' instead of '.'
    """

    return str(number).replace('.', 'dot')


def _custom_log_filename(sensor_id: int, sensor_name: str, sensor_lat: float = None, sensor_lng: float = None) -> str:
    """
    A function that takes a set of sensor parameters and return a custom log filename.
    """

    base_name = f"sensor_{sensor_id}_{name_cleaner(sensor_name)}"
    if sensor_lat is None and sensor_lng is None:
        return base_name
    return f"{base_name}_{number_cleaner(sensor_lat)}_{number_cleaner(sensor_lng)}"


def _custom_logger_format():
    """
    A function that returns the format string for formatting log records.
    """

    return '[TIME]: %(asctime)s - [LEVEL]: %(levelname)s - [DESCRIPTION]: %(message)s'


class FileHandlerRotator(object):
    """
    A class that caches the current file handler and defines the business rules for rotating the handler
    when a different sensor is in use.
    """

    def __init__(
        self,
        logger_name: str,                       # the target logger's name for applying handler rotation.
        logger_level,                           # the desired logging level.
        logger_dir="./",                        # the logging directory path.
        logger_fmt=_custom_logger_format()      # the desired log record format.
    ):
        self._logger_dir = logger_dir
        self._logger_fmt = logger_fmt
        self._logger_name = logger_name
        self._logger_level = logger_level
        self._logger = logging.getLogger(self._logger_name)
        self._cached_file_handler = None

    def _attach_handler(self, filename: str):
        """
        A function that automatically detaches the cached file handler (if any exists) and attaches a new one.

        :param filename:            the new (to attach) file handler's file name.
        """

        if self._cached_file_handler is not None:
            self._detach_handler()

        self._cached_file_handler = logging.FileHandler(filename=self._fullpath(filename))
        self._cached_file_handler.formatter = logging.Formatter(fmt=self._logger_fmt)
        self._cached_file_handler.setLevel(level=self._logger_level)
        self._logger.addHandler(self._cached_file_handler)

    def _fullpath(self, filename: str) -> str:
        """
        A function that computes the fullpath of the current log filename and add the file extension.

        :param filename:            the file handler's filename.
        :return:                    the complete path to the filename (relative to 'airquality' directory).
        """

        return f"{self._logger_dir}/{filename}.log"

    def _detach_handler(self):
        """
        A function that detaches the cached file handler from the logger instance.
        """

        self._logger.removeHandler(self._cached_file_handler)
        self._cached_file_handler = None

    def rotate(self, sensor_ident: SensorIdentity):
        """
        A function that substitutes the cached file handler with a new one associated to the sensor identity.

        :param sensor_ident:                the sensor's information for computing a unique filename in time.
        """

        fname = _custom_log_filename(
            sensor_id=sensor_ident.sensor_id,
            sensor_name=sensor_ident.sensor_name,
            sensor_lat=sensor_ident.sensor_lat,
            sensor_lng=sensor_ident.sensor_lng
        )
        self._attach_handler(
            filename=fname
        )
