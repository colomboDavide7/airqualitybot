######################################################
#
# Author: Davide Colombo
# Date: 22/12/21 15:47
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
from airquality.dbrepo import DBRepository
from airquality.sqldict import MutableSQLDict
from airquality.dbadapter import DBAdapterABC


class PurpleairFactory(object):

    def __init__(self, personality: str, dbadapter: DBAdapterABC, options=()):
        self.personality = personality
        self.dbadapter = dbadapter
        self.options = options
        self._url_template = ""

    @property
    def url_template(self) -> str:
        if not self._url_template:
            self._url_template = os.environ['purpleair_url']
        return self._url_template

    @property
    def sensor_dict(self) -> MutableSQLDict:
        return MutableSQLDict(table=DBRepository.filtered_sensor_table(requested_type=self.personality), dbadapter=self.dbadapter)

    @property
    def apiparam_dict(self) -> MutableSQLDict:
        return MutableSQLDict(table=DBRepository.apiparam_table(), dbadapter=self.dbadapter)

    @property
    def geolocation_dict(self) -> MutableSQLDict:
        return MutableSQLDict(table=DBRepository.geolocation_table(), dbadapter=self.dbadapter)
