#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 12:04
# @Description: this script defines a class for parsing sensor's API timestamps
#
#################################################
import abc
import datetime as dt
from airquality.core.constants.shared_constants import EXCEPTION_HEADER

THINGSPK_FMT = "%Y-%m-%dT%H:%M:%SZ"
ATMOTUBE_FMT = "%Y-%m-%dT%H:%M:%S.000Z"
SQL_TIMEST_FMT = "%Y-%m-%d %H:%M:%S"


class Timestamp(abc.ABC):

    @abc.abstractmethod
    def add_days(self, days: int):
        pass

    @abc.abstractmethod
    def is_after(self, other) -> bool:
        pass


class SQLTimestamp(Timestamp):

    def __init__(self, timestamp: str, fmt: str = SQL_TIMEST_FMT):
        self.ts = timestamp
        self.fmt = fmt

    def add_days(self, days: int):
        my_dt = dt.datetime.strptime(self.ts, self.fmt)
        my_dt = my_dt + dt.timedelta(days=days)
        return SQLTimestamp(my_dt.strftime(SQL_TIMEST_FMT), SQL_TIMEST_FMT)

    def is_after(self, other) -> bool:
        if not isinstance(other, SQLTimestamp):
            raise SystemExit(f"{EXCEPTION_HEADER} {SQLTimestamp.__name__} bad type => cannot compare with object "
                             f"of type='{other.__class__.__name__}'")
        my_dt = dt.datetime.strptime(self.ts, self.fmt)
        other_dt = dt.datetime.strptime(other.ts, other.fmt)
        return (my_dt - other_dt).total_seconds() > 0


class CurrentTimestamp(SQLTimestamp):

    def __init__(self):
        super().__init__(dt.datetime.now().strftime(SQL_TIMEST_FMT), SQL_TIMEST_FMT)

    def add_days(self, days: int):
        return super().add_days(days)

    def is_after(self, other):
        return super().is_after(other)
