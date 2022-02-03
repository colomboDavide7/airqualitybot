# ======================================
# @author:  Davide Colombo
# @date:    2022-01-19, mer, 12:33
# ======================================
from dateutil import tz
from datetime import datetime
from timezonefinder import TimezoneFinderL


_TIMEZONE_FINDER = TimezoneFinderL(in_memory=False)
_TIMEZONE_FINDER.using_numba()


def _timezone_from_coords(latitude: float, longitude: float):
    tzname = _TIMEZONE_FINDER.timezone_at(lng=longitude, lat=latitude)
    return tz.gettz(tzname)


def _timezone_from_name(name: str):
    return tz.gettz(name)


def now_utctz() -> datetime:
    """
    A function that returns the current timestamp in the local time zone.
    """

    utc_dt = datetime.now(tz=tz.tzutc())
    return utc_dt.astimezone().replace(microsecond=0)


def make_naive(time: datetime) -> datetime:
    """
    A function that takes a datetime object and returns the corresponding UTC time zone naive datetime object.
    """

    return time.astimezone(tz=tz.tzutc()).replace(microsecond=0, tzinfo=None)


def make_timezone_aware_UTC(utctime, fmt: str) -> datetime:
    """
    Converting UTC time zone string object to a timezone aware-datetime object in UTC timezone.
    """

    dt = datetime.strptime(utctime, fmt) if fmt else datetime.utcfromtimestamp(utctime)
    return dt.replace(tzinfo=tz.tzutc())


def make_timezone_aware_FROM_COORDS(utctime, latitude: float, longitude: float,  fmt="") -> datetime:
    """
    Converting UTC time zone string object to a timezone aware-datetime object which timezone is computed from coords.
    """

    dt = make_timezone_aware_UTC(utctime, fmt)
    zone = _timezone_from_coords(latitude, longitude)
    return dt.astimezone(tz=zone)


def make_timezone_aware_FROM_NAME(utctime, timezone_name: str, fmt="") -> datetime:
    """
    Converting UTC time zone string object to a timezone aware-datetime object which timezone is computed from coords.
    """

    dt = make_timezone_aware_UTC(utctime, fmt)
    zone = _timezone_from_name(timezone_name)
    return dt.astimezone(tz=zone)


def make_timezone_aware_FROM_LOCAL(utctime, fmt="") -> datetime:
    """
    Converting UTC time zone string object to a timezone aware-datetime object which timezone is computed from coords.
    """

    dt = make_timezone_aware_UTC(utctime, fmt)
    zone = _timezone_from_coords(latitude=45, longitude=9)
    return dt.astimezone(tz=zone)
