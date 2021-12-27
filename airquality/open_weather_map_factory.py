######################################################
#
# Author: Davide Colombo
# Date: 27/12/21 09:53
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
from typing import List
from airquality.program_handler import Option
from airquality.dbadapter import DBAdapterABC
from airquality.dbrepo import DBRepository
from airquality.sqldict import MutableSQLDict, HeavyweightInsertSQLDict, FrozenSQLDict


class OpenWeatherMapFactory(object):

    def __init__(self, personality: str, dbadapter: DBAdapterABC, options: List[Option] = ()):
        self.personality = personality
        self.dbadapter = dbadapter
        self.program_options = options

    # @property
    # def current_weather_dict(self) -> HeavyweightInsertSQLDict:
    #

    @property
    def requested_cities(self):
        if self.program_options:
            return os.environ[f'{self.personality}_cities']
        return ""

    @property
    def requested_country(self):
        if self.program_options:
            return os.environ[f'{self.personality}_country']
        return ""

    @property
    def self_options(self):
        return [opt for opt in self.program_options if opt.pers == self.personality]

    @property
    def url_template(self) -> str:
        return os.environ[f'{self.personality}_url']

    @property
    def service_api_param_dict(self) -> MutableSQLDict:
        service_table = DBRepository.filtered_service_table(requested_type=self.personality)
        apiparam_table = DBRepository.joined_service_api_param(join_table=service_table)
        return MutableSQLDict(table=apiparam_table, dbadapter=self.dbadapter)

    @property
    def geoarea_dict(self) -> FrozenSQLDict:
        geoarea_table = DBRepository.filtered_geoarea_table(requested_cities=self.requested_cities, country=self.requested_country)
        return FrozenSQLDict(table=geoarea_table, dbadapter=self.dbadapter)

    @property
    def measure_param_dict(self) -> FrozenSQLDict:
        measure_param_table = DBRepository.filtered_measure_param_table(requested_param=self.personality)
        return FrozenSQLDict(table=measure_param_table, dbadapter=self.dbadapter)
