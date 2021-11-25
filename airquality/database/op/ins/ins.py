######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:19
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.database.op.baseop as base
import airquality.database.util.conn as connection
import airquality.database.util.query as query


class InsertWrapper(base.DatabaseWrapper, abc.ABC):

    def __init__(self, conn: connection.DatabaseAdapter, builder: query.QueryBuilder, log_filename="log"):
        super(InsertWrapper, self).__init__(conn=conn, builder=builder, log_filename=log_filename)
        self.query_to_execute = ""

    def insert(self) -> None:
        self.database_conn.send(self.query_to_execute)
