######################################################
#
# Author: Davide Colombo
# Date: 11/12/21 17:57
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import abc
from typing import Dict, List
from collections import namedtuple
import airquality.env.fact as factabc

ChannelType = namedtuple('Channel', ['sensor_id', 'apikey', 'ident', 'name', 'last_timest'])


# ------------------------------- APIEnvFactABC ------------------------------- #
class APIEnvFactABC(factabc.EnvFactABC, abc.ABC):

    def __init__(self, path_to_env: str, command: str, target: str):
        super(APIEnvFactABC, self).__init__(path_to_env=path_to_env, target=target, command=command)
        self._url_template = None
        self._api_fmt = None

    @property
    def url(self) -> str:
        if self._url_template is None:
            try:
                self._url_template = os.environ[f'{self.target}_url']
            except KeyError as err:
                raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} => {err!r}")
        return self._url_template

    @property
    def fmt(self) -> str:
        if self._api_fmt is None:
            try:
                self._api_fmt = os.environ[f'{self.target}_response_fmt']
            except KeyError as err:
                raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} => {err!r}")
        return self._api_fmt

    @property
    def measure_param(self) -> Dict[str, int]:
        meas_param_query = self.sql_queries.s5.format(personality=self.target)
        db_lookup = self.db_conn.execute(meas_param_query)
        return {param_code: param_id for param_code, param_id in db_lookup}

    @property
    def api_param(self) -> List[ChannelType]:
        query2exec = self.sql_queries.s12.format(target=self.target)
        sensor_lookup = self.db_conn.execute(query2exec)
        sensor_id_string = ','.join(f"{item[0]}" for item in sensor_lookup)
        query2exec = self.sql_queries.s2.format(ids=sensor_id_string)
        api_param_lookup = self.db_conn.execute(query2exec)
        for ap in api_param_lookup:
            yield ap

        # return [ChannelType(sensor_id=id_, apikey=key, ident=ident, name=name, last_timest=tstype.datetime2sqltimest(dt))
        #         for  in api_param_lookup]
