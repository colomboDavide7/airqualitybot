######################################################
#
# Author: Davide Colombo
# Date: 06/12/21 19:06
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.database.conn.adapt as adapt
import airquality.database.util.query as qry


class DatabaseRepo(abc.ABC):

    def __init__(self, db_adapter: adapt.DatabaseAdapter, query_builder: qry.QueryBuilder):
        self.db_adapter = db_adapter
        self.query_builder = query_builder

    @abc.abstractmethod
    def lookup(self):
        pass

    @abc.abstractmethod
    def push(self, responses) -> None:
        pass
