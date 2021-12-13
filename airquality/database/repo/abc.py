######################################################
#
# Author: Davide Colombo
# Date: 06/12/21 19:06
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.database.conn.adapt as adapt
import airquality.file.json as filetype


class DatabaseRepoABC(abc.ABC):

    def __init__(self, db_adapter: adapt.DatabaseAdapter, sql_queries: filetype.JSONFile):
        self.db_adapter = db_adapter
        self.sql_queries = sql_queries

    @abc.abstractmethod
    def lookup(self):
        pass

    ################################ push() ###############################
    def push(self, query2exec: str) -> None:
        self.db_adapter.send(query2exec)
