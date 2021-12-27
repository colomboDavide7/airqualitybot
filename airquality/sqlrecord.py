######################################################
#
# Author: Davide Colombo
# Date: 24/12/21 16:34
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict
from abc import abstractmethod
from itertools import count, islice
from collections import namedtuple


class MeasureSQLRecord(object):

    def __init__(self, record_id: int, packet_id: int, code2id: Dict[str, int], values: Dict[str, str]):
        self.record_id = record_id
        self.packet_id = packet_id
        self.code2id = code2id

    @abstractmethod
    def sql_record(self) -> str:
        pass


class MobileSQLRecord(MeasureSQLRecord):

    def sql_record(self) -> str:
        return f"({self.record_id}, {self.packet_id}, {code2id[code]}, {wrap_value(val)}, '{item.measured_at()}', {item.located_at()})"


class StationSQLRecord(MeasureSQLRecord):

    def __init__(self, sensor_id: int):
        self.sensor_id = sensor_id

    def sql_record(self) -> str:
        return f"({self.record_id}, {self.packet_id}, {self.sensor_id}, {code2id[code]}, {wrap_value(val)}, '{item.measured_at()}')"




def wrap_value(value: str, default="NULL") -> str:
    return f"'{value}'" if value is not None else default


from collections import Iterable


class SQLRecords(Iterable, ABC):

    def __init__(self, start_record_id: int, measure_param: Dict[str, int], record_factory):
        self.start_record_id = start_record_id
        self._record_id_counter = count(self.start_record_id)
        self.measure_param = measure_param
        self.record_factory = record_factory

    @property
    def record_id(self):
        return next(self._record_id_counter)

    @abstractmethod
    def sql_records(self):
        pass

    def __getitem__(self, index):
        if index >= len(self):
            raise IndexError(f"{type(self).__name__} in __getitem__(): expected '{index}' to be at most {len(self)-1}")
        return next(islice(self.sql_records(), index, None))

    def __iter__(self):
        return self.sql_records()

    def __len__(self):
        return sum(1 for _ in self.sql_records())


class AtmotubeSQLRecords(SQLRecords):

    def __init__(self, start_record_id: int, measure_param: Dict[str, int], record_factory=MobileSQLRecord):
        super(AtmotubeSQLRecords, self).__init__(
            start_record_id=start_record_id, measure_param=measure_param, record_factory=record_factory
        )

    def sql_records(self):
        return (self.record_factory(record_id=self.record_id, packet_id=idx, item) for idx, item in enumerate(self.items))


class ThingspeakSQLRecords(SQLRecords):

    def __init__(self, start_record_id: int, measure_param: Dict[str, int], sensor_id: int, record_factory=StationSQLRecord):
        super(ThingspeakSQLRecords, self).__init__(
            start_record_id=start_record_id, measure_param=measure_param, record_factory=record_factory
        )
        self.sensor_id = sensor_id

    def sql_records(self):
        return (self.record_factory(record_id=self.record_id, idx, item, sensor_id=self.sensor_id) for idx, item in enumerate(self.items))
