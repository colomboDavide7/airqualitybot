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


def get_timestamp_class(sensor_type: str):

    if sensor_type == 'atmotube':
        return AtmotubeTimestamp
    elif sensor_type == 'thingspeak':
        return ThingspeakTimestamp
    elif sensor_type == 'purpleair':
        return UnixTimestamp
    else:
        raise SystemExit(f"'{get_timestamp_class.__name__}():' bad type '{sensor_type}'")


################################ TIMESTAMP CLASS ################################
class Timestamp(abc.ABC):

    def __init__(self, timestamp: str, fmt: str = SQL_TIMEST_FMT):
        self.ts = timestamp
        self.fmt = fmt

    @abc.abstractmethod
    def add_days(self, days: int):
        pass

    @abc.abstractmethod
    def is_after(self, other) -> bool:
        pass


################################ SQL TIMESTAMP CLASS ################################
class SQLTimestamp(Timestamp):

    def __init__(self, timestamp: str, fmt: str = SQL_TIMEST_FMT):
        super(SQLTimestamp, self).__init__(timestamp=timestamp, fmt=fmt)

    def add_days(self, days: int):
        my_dt = dt.datetime.strptime(self.ts, self.fmt)
        my_dt = my_dt + dt.timedelta(days=days)
        return SQLTimestamp(my_dt.strftime(SQL_TIMEST_FMT), SQL_TIMEST_FMT)

    def is_after(self, other) -> bool:
        if not isinstance(other, SQLTimestamp):
            raise SystemExit(
                f"{SQLTimestamp.__name__}: bad type => cannot compare with object of type='{other.__class__.__name__}'")

        self_dt = dt.datetime.strptime(self.ts, self.fmt)
        other_dt = dt.datetime.strptime(other.ts, other.fmt)
        return (self_dt - other_dt).total_seconds() > 0

    def is_same_day(self, other) -> bool:
        if not isinstance(other, SQLTimestamp):
            raise SystemExit(f"{SQLTimestamp.__name__}: bad type => cannot compare with object of "
                             f"type='{other.__class__.__name__}'")

        self_dt = dt.datetime.strptime(self.ts, self.fmt).date()
        other_dt = dt.datetime.strptime(other.ts, other.fmt).date()
        return self_dt.__eq__(other_dt)


################################ ATMOTUBE TIMESTAMP CLASS ################################
class AtmotubeTimestamp(SQLTimestamp):

    def __init__(self, timestamp: str, fmt: str = ATMOTUBE_FMT):
        super(AtmotubeTimestamp, self).__init__(timestamp=dt.datetime.strptime(timestamp, fmt).strftime(SQL_TIMEST_FMT))

    def add_days(self, days: int = 1):
        super().add_days(days)

    def is_after(self, other) -> bool:
        return super().is_after(other)
    
    def is_same_day(self, other) -> bool:
        return super(AtmotubeTimestamp, self).is_same_day(other)


################################ THINGSPEAK TIMESTAMP CLASS ################################
class ThingspeakTimestamp(SQLTimestamp):

    def __init__(self, timestamp: str, fmt: str = THINGSPK_FMT):
        super(ThingspeakTimestamp, self).__init__(timestamp=dt.datetime.strptime(timestamp, fmt).strftime(SQL_TIMEST_FMT))

    def add_days(self, days: int = 7):
        super().add_days(days)

    def is_after(self, other) -> bool:
        return super().is_after(other)

    def is_same_day(self, other) -> bool:
        return super(ThingspeakTimestamp, self).is_same_day(other)


################################ CURRENT TIMESTAMP CLASS ################################
class CurrentTimestamp(SQLTimestamp):

    def __init__(self):
        super().__init__(timestamp=dt.datetime.now().strftime(SQL_TIMEST_FMT), fmt=SQL_TIMEST_FMT)

    def add_days(self, days: int):
        return super().add_days(days)

    def is_after(self, other):
        return super().is_after(other)

    def is_same_day(self, other) -> bool:
        return super(CurrentTimestamp, self).is_same_day(other)


################################ UNIX TIMESTAMP CLASS ################################
class UnixTimestamp(SQLTimestamp):

    def __init__(self, unixts: int, fmt: str = SQL_TIMEST_FMT):
        super(UnixTimestamp, self).__init__(timestamp=dt.datetime.fromtimestamp(unixts).strftime(SQL_TIMEST_FMT),
                                            fmt=fmt)

    def add_days(self, days: int):
        return super().add_days(days)

    def is_after(self, other) -> bool:
        return super().is_after(other)

    def is_same_day(self, other) -> bool:
        return super(UnixTimestamp, self).is_same_day(other)
