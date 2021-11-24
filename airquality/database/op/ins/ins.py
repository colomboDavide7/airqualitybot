######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:19
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List
import airquality.database.op.baseop as base
import airquality.database.util.conn as connection
import airquality.database.util.query as query
import airquality.database.rec.baserec as baserec


class InsertWrapper(base.DatabaseOperationWrapper, abc.ABC):

    def __init__(self, conn: connection.DatabaseAdapter, query_builder: query.QueryBuilder, log_filename="log"):
        super(InsertWrapper, self).__init__(conn=conn, query_builder=query_builder, log_filename=log_filename)
        self.conn = conn
        self.query_builder = query_builder

    @abc.abstractmethod
    def insert(self, records: List[baserec.BaseRecord]) -> None:
        pass
