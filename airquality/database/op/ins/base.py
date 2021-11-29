######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:19
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.database.op.baseop as base
import airquality.database.conn.adapt as db
import airquality.database.util.query as query


class InsertWrapper(base.DatabaseWrapper, abc.ABC):

    def __init__(self, conn: db.DatabaseAdapter, builder: query.QueryBuilder, record_builder, log_filename="log"):
        super(InsertWrapper, self).__init__(conn=conn, builder=builder, log_filename=log_filename)
        self.record_builder = record_builder

    @abc.abstractmethod
    def insert(self, api_responses) -> None:
        pass
