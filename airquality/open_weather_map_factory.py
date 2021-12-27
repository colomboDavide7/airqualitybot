######################################################
#
# Author: Davide Colombo
# Date: 27/12/21 09:53
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os

from airquality.dbadapter import DBAdapterABC
from airquality.dbrepo import DBRepository
from airquality.sqltable import FilterSQLTable
from airquality.sqldict import MutableSQLDict, HeavyweightInsertSQLDict, FrozenSQLDict


class OpenWeatherMapFactory(object):

    def __init__(self, personality: str, dbadapter: DBAdapterABC, options=()):
        self.personality = personality
        self.dbadapter = dbadapter
        self.program_options = options

    # @property
    # def current_weather_dict(self) -> HeavyweightInsertSQLDict:
    #

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
        geoarea_table = DBRepository.filtered_geoarea_table()
        print(repr(geoarea_table))
        return FrozenSQLDict(table=geoarea_table, dbadapter=self.dbadapter)
