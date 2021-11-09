#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 12:04
# @Description: this script defines a class for parsing sensor's API timestamps
#
#################################################
import re
import abc
import datetime as dt
from airquality.constants.shared_constants import EXCEPTION_HEADER

THINGSPK_FMT = "%Y-%m-%dT%H:%M:%SZ"
ATMOTUBE_FMT = "%Y-%m-%dT%H:%M:%S.000Z"
SQL_TIMEST_FMT = "%Y-%m-%d %H:%M:%S"
ATMOTUBE_REGEX = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d+Z'
THINGSPK_REGEX = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z'


class Timestamp(abc.ABC):

    @abc.abstractmethod
    def add_days(self, days: int):
        pass

    @abc.abstractmethod
    def is_before(self, other) -> bool:
        pass


class AtmotubeTimestamp(Timestamp):

    def __init__(self, timestamp: str):
        if not re.match(re.compile(ATMOTUBE_REGEX), timestamp):
            raise SystemExit(
                f"{EXCEPTION_HEADER} {AtmotubeTimestamp.__name__} bad timestamp => '{timestamp}' is not valid"
            )
        tmp = timestamp.strip('Z')
        tmp, zone = tmp.split('.')
        self.ts = tmp.replace('T', ' ')

    def add_days(self, days: int):
        my_dt = dt.datetime.strptime(self.ts, SQL_TIMEST_FMT)
        my_dt = my_dt + dt.timedelta(days=days)
        return AtmotubeTimestamp(timestamp=my_dt.strftime(ATMOTUBE_FMT))

    def is_before(self, other) -> bool:
        if not isinstance(other, AtmotubeTimestamp):
            raise SystemExit(f"{EXCEPTION_HEADER} {AtmotubeTimestamp.__name__} bad type => cannot compare with object "
                             f"of type='{other.__class__.__name__}'")
        my_dt = dt.datetime.strptime(self.ts, SQL_TIMEST_FMT)
        other_dt = dt.datetime.strptime(other.ts, SQL_TIMEST_FMT)
        return (my_dt - other_dt).total_seconds() < 0


class ThingspeakTimestamp(Timestamp):

    def __init__(self, timestamp: str):
        if not re.match(re.compile(THINGSPK_REGEX), timestamp):
            raise SystemExit(
                f"{EXCEPTION_HEADER} {ThingspeakTimestamp.__name__} bad timestamp => '{timestamp}' is not valid"
            )
        tmp = timestamp.strip('Z')
        self.ts = tmp.replace('T', ' ')

    def add_days(self, days: int):
        my_dt = dt.datetime.strptime(self.ts, SQL_TIMEST_FMT)
        my_dt = my_dt + dt.timedelta(days=days)
        return ThingspeakTimestamp(timestamp=my_dt.strftime(THINGSPK_FMT))

    def is_before(self, other) -> bool:
        if not isinstance(other, ThingspeakTimestamp):
            raise SystemExit(f"{EXCEPTION_HEADER} {ThingspeakTimestamp.__name__} bad type => cannot compare with object "
                             f"of type='{other.__class__.__name__}'")
        my_dt = dt.datetime.strptime(self.ts, SQL_TIMEST_FMT)
        other_dt = dt.datetime.strptime(other.ts, SQL_TIMEST_FMT)
        return (my_dt - other_dt).total_seconds() < 0
