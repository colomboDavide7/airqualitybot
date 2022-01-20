# ======================================
# @author:  Davide Colombo
# @date:    2022-01-19, mer, 12:33
# ======================================
import logging
from dateutil import tz
from datetime import datetime, tzinfo, timezone
from timezonefinder import TimezoneFinder


class TimestConversionError(Exception):
    """
    A subclass of Exception that is raised by *Timest* class.
    """
    pass


class Timest(object):
    """
    A class that defines the business logic for date and timestamp manipulation.

    Keyword arguments:
        *input_fmt*                 the expected format for the input date or timestamp objects (defaults to None).
        *output_fmt*                the desired format for the output date or timestamp objects (defaults to None).

    Raises:
        *TimestConversionError*     this exception is raised to signal an invalid usage of this class.

    If *input_fmt* is None, this class expects that all the *time* to be formatted are UNIX timestamp (float)

    If *output_fmt* is None, the output is a UNIX timestamp (float).

    An *input_fmt* equal to None with an *output_fmt* not None (str) means that the input time is a UNIX timestamp
    and will be outputted to the desired format.

    And vice-versa.

    """

    def __init__(self, input_fmt: str = None, output_fmt: str = None):
        self._input_fmt = input_fmt
        self._output_fmt = output_fmt
        self._tz_finder = TimezoneFinder()
        self._logger = logging.getLogger(__name__)

    def _raise(self, cause: str):
        self._logger.exception(cause)
        raise TimestConversionError(cause)

    @classmethod
    def current_utc_timetz(cls) -> datetime:
        """
        A class method that returns the current timestamp in the local time zone.
        """
        utc_dt = datetime.now(tz=timezone.utc)
        return utc_dt.astimezone().replace(microsecond=0)

    def utc_time2utc_timetz(self, time, latitude: float, longitude: float) -> datetime:
        """
        Converting UTC time zone *time* into the corresponding UTC geolocation's time zone.
        """
        dt = self._safe_strpin(time)
        dt_tz = dt.replace(tzinfo=tz.tzutc())
        return dt_tz.astimezone(tz=self._tzinfo_from(lat=latitude, lng=longitude))

    def strfout(self, dt: datetime) -> str:
        """
        :param dt:                          the datetime object to format.
        :return:                            the formatted datetime object according to *output_fmt* value.
        """
        return self._safe_strfout(dt)

    def _safe_strfout(self, dt: datetime) -> str:
        """
        :raises TimestConversionError:      if try to format *dt* when *output_fmt* is None.
        :param dt:                          the datetime to format.
        :return:                            the formatted *dt* object according to *output_fmt* value.
        """

        if self._output_fmt is None:
            self._raise(cause="[FATAL] expected *output_fmt* to be not None!!!")
        return dt.strftime(self._output_fmt)

    def _safe_strpin(self, time) -> datetime:
        """
        This method decide which parsing method to call based on the *input_fmt* value.

        :param time:                        the time input object to convert.
        :return:                            the *datetime* object that represents the converted *time*.
        """

        if self._input_fmt is not None:
            return self._safe_strptime(time)
        return self._safe_utcfromtimestamp(time)

    def _safe_utcfromtimestamp(self, time) -> datetime:
        """
        This method handles the conversion from UNIX timestamp to *datetime* object.

        :raises TimestConversionError:      if *time* is not of <class float>.
        :param time:                        the UNIX timestamp to convert.
        :return:                            the *datetime* object that corresponds to *time* timestamp.
        """

        if not isinstance(time, (float, int)):
            self._raise(cause=f"[FATAL] expected '{time}' to be of type <class float>!!!")
        return datetime.utcfromtimestamp(time)

    def _safe_strptime(self, time) -> datetime:
        """
        This method handles the conversion from string to *datetime* object.

        :raises TimestConversionError:      if *time* is not of <class str>.
        :raises TimestConversionError:      if *time* does not match *input_fmt*
        :param time:                        the string time to convert.
        :return:                            the *datetime* object that correspond to the *time* string.
        """

        if not isinstance(time, str):
            self._raise(cause=f"[FATAL] expected '{time}' to be of type <class str>!!!")
        try:
            return datetime.strptime(time, self._input_fmt)
        except ValueError as err:
            self._raise(cause=str(err))

    def _tzinfo_from(self, lat: float, lng: float) -> tzinfo:
        """
        This method converts a geolocation into a *tzinfo* object.

        :param lat:                     latitude in decimal degrees.
        :param lng:                     longitude in decimal degrees.
        :return:                        the *tzinfo* object that corresponds to time zone at the given location.
        """

        tzname = self._tz_finder.timezone_at(lat=lat, lng=lng)
        return tz.gettz(tzname)


DEFAULT_OUT_FMT = "%Y-%m-%d %H:%M:%S%z"
ATMOTUBE_FMT    = "%Y-%m-%dT%H:%M:%S.%fZ"
THINGSPEAK_FMT  = "%Y-%m-%dT%H:%M:%SZ"


def purpleair_timest(output_fmt=DEFAULT_OUT_FMT) -> Timest:
    """
    Constructor function that return a ready-to-use *Timest* object compliant to PurpleAir timestamp format.
    """

    return Timest(output_fmt=output_fmt)


def atmotube_timest(output_fmt=DEFAULT_OUT_FMT) -> Timest:
    """
    Constructor function that return a ready-to-use *Timest* object compliant to Atmotube timestamp format.
    """

    return Timest(input_fmt=ATMOTUBE_FMT, output_fmt=output_fmt)


def thingspeak_timest(output_fmt=DEFAULT_OUT_FMT) -> Timest:
    """
    Constructor function that return a ready-to-use *Timest* object compliant to Thingspeak timestamp format.
    """

    return Timest(input_fmt=THINGSPEAK_FMT, output_fmt=output_fmt)
