# ======================================
# @author:  Davide Colombo
# @date:    2022-01-19, mer, 12:33
# ======================================
import logging
from dateutil import tz
from datetime import datetime, tzinfo, timezone
from timezonefinder import TimezoneFinderL
from abc import ABC, abstractmethod


# =========== TIMEZONE MAKER (SUPPORT CLASS)
class TimezoneMaker(ABC):
    """
    AbstractBaseClass that defines an interface for computing time zone in different ways.
    """

    @abstractmethod
    def tzinfo(self):
        pass


class _RotatingTimezone(TimezoneMaker):
    """
    A class that implements the *TimezoneMaker* interface by computing the time zone of different any locations.

    The term 'rotating' refers to this behavior.

    Constraints: before calling *tzinfo* method it must be called the *set_timezone* method to set
                 the new desired coordinates to compute the timezone offset.
    """

    def __init__(self):
        self._tzfinder = TimezoneFinderL(in_memory=False)
        self._tzfinder.using_numba()
        self._lat = None
        self._lng = None
        self._tzname = None

    def set_timezone(self, lat: float = None, lng: float = None, tz_name: str = None):
        if lat is not None and lng is not None:
            self._lat = lat
            self._lng = lng
            self._tzname = None
        elif tz_name is not None:
            self._lat = self._lng = None
            self._tzname = tz_name
        else:
            raise ValueError(
                "CANNOT PICK METHOD FOR BUILDING THE TIME ZONE INFO: "
                "expected latitude and longitude or time zone name to be not None."
            )

    def tzinfo(self):
        tmp_tzname = self._tzname
        if self._lat is not None and self._lng is not None:
            tmp_tzname = self._tzfinder.timezone_at(lat=self._lat, lng=self._lng)
        return tz.gettz(tmp_tzname)


class _FixedTimezone(TimezoneMaker):
    """
    A class that implements the *TimezoneMaker* interface and persistently provide a specific time zone offset.

    Keyword arguments:
        *latitude*                      the time zone's latitude in decimal degrees (-90.0, +90.0)
        *longitude*                     the time zone' longitude in decimal degrees (-180.0, +180.0)

    """

    def __init__(self, latitude: float, longitude: float):
        self._lat = latitude
        self._lng = longitude
        self._cached_tzinfo = None

    def tzinfo(self):
        if self._cached_tzinfo is None:
            tzfinder = TimezoneFinderL(in_memory=False)
            tzfinder.using_numba()
            tzname = tzfinder.timezone_at(lat=self._lat, lng=self._lng)
            self._cached_tzinfo = tz.gettz(tzname)
        return self._cached_tzinfo


class _FixedTimezoneWithName(TimezoneMaker):
    """
    A class that implements the *TimezoneMaker* interface and persistently provide a time zone offset using the
    time zone name passed as argument.
    """

    def __init__(self, tz_name: str):
        self._tz_name = tz_name
        self._cached_tzinfo = None

    def tzinfo(self):
        if not self._cached_tzinfo:
            self._cached_tzinfo = tz.gettz(self._tz_name)
        return self._cached_tzinfo


class TimestConversionError(Exception):
    """
    A subclass of Exception that is raised by *Timest* class.
    """
    pass


def _init_tzmaker(lat: float, lng: float, tz_name: str):
    if lat is not None and lng is not None:
        return _FixedTimezone(latitude=lat, longitude=lng)
    elif tz_name is not None:
        return _FixedTimezoneWithName(tz_name=tz_name)
    else:
        return _RotatingTimezone()


class Timest(object):
    """
    A class that defines the business logic for time zone's date and timestamp manipulation.

    Keyword arguments:
        *input_fmt*                 the expected format for the input date or timestamp objects (defaults to None).
        *output_fmt*                the desired format for the output date or timestamp objects (defaults to None).
        *latitude*                  the latitude in decimal degrees of the desired time zone.
        *longitude*                 the longitude in decimal degrees of the desired time zone.
        *tz_name*                   the string representation of the time zone.

    Raises:
        *TimestConversionError*     this exception is raised to signal an invalid usage of this class.

    Settings: if BOTH *latitude* and *longitude* are passed to __init__, this class will shift every date using
              the pre-computed time zone offset according to *latitude* and *longitude* values. Same for the case
              of passing *tz_name* to __init__ method.

              In case both *latitude* and *longitude* and *tz_name* are passed, the first two has the precedence.

              Otherwise, this class assumes that a 'rotating' time zone will be used.
              The term 'rotating' refers to the fact that the class will compute the time zone offset on the fly,
              and this may slow down a little the program.

    If *input_fmt* is None, this class expects that all the input time to be formatted are UNIX timestamp (float).

    If *output_fmt* is None, this class will output-format input time as UNIX timestamp (float).

    An *input_fmt* equal to None with an *output_fmt* not None (str) means that the input time is a UNIX timestamp
    and will be outputted to the desired format.

    And vice-versa.

    """

    def __init__(
        self,
        input_fmt: str = None,
        output_fmt: str = None,
        latitude: float = None,
        longitude: float = None,
        tz_name: str = None
    ):
        self._logger = logging.getLogger(__name__)
        self._input_fmt = input_fmt
        self._output_fmt = output_fmt
        self._tzmaker = _init_tzmaker(lat=latitude, lng=longitude, tz_name=tz_name)

    @classmethod
    def current_utc_timetz(cls) -> datetime:
        """
        A class method that returns the current timestamp in the local time zone.
        """
        utc_dt = datetime.now(tz=timezone.utc)
        return utc_dt.astimezone().replace(microsecond=0)

    def utc_time2utc_tz(self, time) -> datetime:
        """
        Converting UTC time zone *time* without the time zone into a UTC with time zone.
        """
        dt = self._safe_strpin(time)
        return dt.replace(tzinfo=tz.tzutc())

    def utc_time2utc_localtz(
            self,
            time,                               # the time object to convert (str or float).
            latitude: float = None,             # the time zone's latitude in decimal degrees.
            longitude: float = None,            # the time zone's longitude in decimal degrees.
            tzname: str = None                  # the time zone's name.
    ) -> datetime:
        """
        Converting UTC time zone *time* into the corresponding UTC time shifted by the desired time zone offset.
        """
        utc_dt_tz = self.utc_time2utc_tz(time=time)
        tz_info = self._safe_tzinfo(
            lat=latitude,
            lng=longitude,
            tz_name=tzname
        )
        return utc_dt_tz.astimezone(tz=tz_info)

# =========== TIMEZONE COMPUTATION METHODS
    def _safe_tzinfo(self, lat: float = None, lng: float = None, tz_name: str = None) -> tzinfo:
        """
        This method converts a geolocation into a *tzinfo* object. Latitude and longitude method has the priority
        on the time zone name method.

        :param lat:                     latitude in decimal degrees.
        :param lng:                     longitude in decimal degrees.
        :param tz_name:                 time zone name.
        :return:                        the *tzinfo* object corresponding to the given location.
        """

        if (lat is not None and lng is not None) or \
           tz_name is not None:
            return self._safe_onthefly_tzinfo(lat=lat, lng=lng, tzname=tz_name)
        return self._safe_cached_tzinfo()

    def _safe_onthefly_tzinfo(self, lat: float, lng: float, tzname: str) -> tzinfo:
        """
        Safely assert that this class was configured with *_RotatingTimezone* class for computing the tzinfo.

        :param lat:                     latitude in decimal degrees.
        :param lng:                     longitude in decimal degrees.
        :return:                        the *tzinfo* object corresponding to the given location.
        """

        if not isinstance(self._tzmaker, _RotatingTimezone):
            self._raise(f"expected time zone maker to be of type '{_RotatingTimezone.__name__}'")
        self._tzmaker.set_timezone(lat=lat, lng=lng, tz_name=tzname)
        return self._tzmaker.tzinfo()

    def _safe_cached_tzinfo(self) -> tzinfo:
        """
        Safely verify that this class was configured with *_FixedTimezone* or *_FixedTimezoneWithName* class
        for computing the time zone info object.

        :return:                        the pre-computed *tzinfo* corresponding to the location at configuration time.
        """

        if not isinstance(self._tzmaker, (_FixedTimezone, _FixedTimezoneWithName)):
            self._raise(f"expected time zone maker to be of type '_FixedTimezone*'")
        return self._tzmaker.tzinfo()

# =========== TIME FORMATTER METHODS
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

# =========== EXCEPTION METHOD
    def _raise(self, cause: str):
        self._logger.exception(cause)
        raise TimestConversionError(cause)


DEFAULT_OUT_FMT = "%Y-%m-%d %H:%M:%S%z"
ATMOTUBE_FMT    = "%Y-%m-%dT%H:%M:%S.%fZ"
THINGSPEAK_FMT  = "%Y-%m-%dT%H:%M:%SZ"


# =========== PREDEFINES CONSTRUCTORS
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

    # TODO: add latitude and longitude formal parameters

    return Timest(input_fmt=THINGSPEAK_FMT, output_fmt=output_fmt, latitude=45, longitude=9)
