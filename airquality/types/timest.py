#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 12:04
# @Description: this script defines a class for parsing sensor's API timestamps
#
#################################################
import abc
import datetime as dt

THINGSPK_FMT = "%Y-%m-%dT%H:%M:%SZ"
ATMOTUBE_FMT = "%Y-%m-%dT%H:%M:%S.000Z"
SQL_TIMEST_FMT = "%Y-%m-%d %H:%M:%S"


# ------------------------------- TimestampABC ------------------------------- #
class TimestABC(abc.ABC):

    def __init__(self, timest: str, fmt: str = SQL_TIMEST_FMT):
        self._ts = timest
        self._fmt = fmt

    @property
    def ts(self) -> str:
        my_dt = dt.datetime.strptime(self._ts, self._fmt)
        return my_dt.strftime(SQL_TIMEST_FMT)

    @abc.abstractmethod
    def add_days(self, days: int):
        pass

    @abc.abstractmethod
    def is_after(self, other) -> bool:
        pass


# ------------------------------- SQLTimestamp ------------------------------- #
class SQLTimest(TimestABC):

    def __init__(self, timest: str, fmt: str = SQL_TIMEST_FMT):
        super(SQLTimest, self).__init__(timest=timest, fmt=fmt)

    def add_days(self, days: int) -> TimestABC:
        my_dt = dt.datetime.strptime(self._ts, self._fmt)
        my_dt = my_dt + dt.timedelta(days=days)
        return SQLTimest(my_dt.strftime(SQL_TIMEST_FMT), SQL_TIMEST_FMT)

    def is_after(self, other) -> bool:
        if not isinstance(other, SQLTimest):
            raise SystemExit(f"{self.__class__.__name__} cannot be compared with object of type='{other.__class__.__name__}'")

        self_dt = dt.datetime.strptime(self._ts, self._fmt)
        other_dt = dt.datetime.strptime(other._ts, other._fmt)
        return (self_dt - other_dt).total_seconds() > 0

    def is_same_day(self, other) -> bool:
        if not isinstance(other, SQLTimest):
            raise SystemExit(f"{self.__class__.__name__} cannot be compared with object of type='{other.__class__.__name__}'")

        self_dt = dt.datetime.strptime(self._ts, self._fmt).date()
        other_dt = dt.datetime.strptime(other._ts, other._fmt).date()
        return self_dt.__eq__(other_dt)


# ------------------------------- AtmotubeSQLTimest ------------------------------- #
class AtmotubeSQLTimest(SQLTimest):

    def __init__(self, timest: str, fmt: str = ATMOTUBE_FMT):
        super(AtmotubeSQLTimest, self).__init__(timest=dt.datetime.strptime(timest, fmt).strftime(SQL_TIMEST_FMT))

    def add_days(self, days: int = 1) -> TimestABC:
        return super().add_days(days)

    def is_after(self, other) -> bool:
        return super().is_after(other)
    
    def is_same_day(self, other) -> bool:
        return super(AtmotubeSQLTimest, self).is_same_day(other)


# ------------------------------- ThingspeakSQLTimest ------------------------------- #
class ThingspeakSQLTimest(SQLTimest):

    def __init__(self, timest: str, fmt: str = THINGSPK_FMT):
        super(ThingspeakSQLTimest, self).__init__(timest=dt.datetime.strptime(timest, fmt).strftime(SQL_TIMEST_FMT))

    def add_days(self, days: int = 7) -> TimestABC:
        return super().add_days(days)

    def is_after(self, other) -> bool:
        return super().is_after(other)

    def is_same_day(self, other) -> bool:
        return super(ThingspeakSQLTimest, self).is_same_day(other)


# ------------------------------- CurrentSQLTimest ------------------------------- #
class CurrentSQLTimest(SQLTimest):

    def __init__(self):
        super(CurrentSQLTimest, self).__init__(timest=dt.datetime.now().strftime(SQL_TIMEST_FMT), fmt=SQL_TIMEST_FMT)

    def add_days(self, days: int) -> TimestABC:
        return super().add_days(days)

    def is_after(self, other):
        return super().is_after(other)

    def is_same_day(self, other) -> bool:
        return super(CurrentSQLTimest, self).is_same_day(other)


# ------------------------------- UnixSQLTimest ------------------------------- #
class UnixSQLTimest(SQLTimest):

    def __init__(self, timest: int, fmt: str = SQL_TIMEST_FMT):
        super(UnixSQLTimest, self).__init__(timest=dt.datetime.fromtimestamp(timest).strftime(SQL_TIMEST_FMT), fmt=fmt)

    def add_days(self, days: int) -> TimestABC:
        return super().add_days(days)

    def is_after(self, other) -> bool:
        return super().is_after(other)

    def is_same_day(self, other) -> bool:
        return super(UnixSQLTimest, self).is_same_day(other)


################################ datetime2sqltimest() ################################
def datetime2sqltimest(datetime_: dt.datetime) -> SQLTimest:
    return SQLTimest(timest=datetime_.strftime(SQL_TIMEST_FMT), fmt=SQL_TIMEST_FMT)
