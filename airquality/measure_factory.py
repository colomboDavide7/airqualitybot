######################################################
#
# Author: Davide Colombo
# Date: 23/12/21 09:05
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
from abc import ABC, abstractmethod
from airquality.dbrepo import DBRepository
from airquality.dbadapter import DBAdapterABC
from airquality.sqltable import SQLTable
from airquality.sqldict import HeavyweightInsertSQLDict, FrozenSQLDict, MutableSQLDict


class MeasureFactory(ABC):

    def __init__(self, personality: str, dbadapter: DBAdapterABC, options=()):
        self.personality = personality
        self.dbadapter = dbadapter
        self.options = options

    @abstractmethod
    def measure_table(self) -> SQLTable:
        pass

    @property
    def url_template(self) -> str:
        return os.environ[f'{self.personality}_url']

    @property
    def measure_dict(self) -> HeavyweightInsertSQLDict:
        return HeavyweightInsertSQLDict(table=self.measure_table(), dbadapter=self.dbadapter)

    @property
    def measure_param_dict(self) -> FrozenSQLDict:
        return FrozenSQLDict(
            table=DBRepository.filtered_measure_param_table(requested_param=self.personality), dbadapter=self.dbadapter
        )

    @property
    def apiparam_dict(self) -> MutableSQLDict:
        join_table = DBRepository.filtered_sensor_table(requested_type=self.personality)
        return MutableSQLDict(
            table=DBRepository.joined_sensor_api_param_table(join_table=join_table), dbadapter=self.dbadapter
        )


class AtmotubeFactory(MeasureFactory):

    def measure_table(self) -> SQLTable:
        return DBRepository.mobile_measure_table()


class ThingspeakFactory(MeasureFactory):

    def measure_table(self) -> SQLTable:
        return DBRepository.station_measure_table()
