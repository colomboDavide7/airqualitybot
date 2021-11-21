######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:19
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict, Any
import airquality.database.operation.base as base
import airquality.database.util.conn as connection
import airquality.database.util.query as query


class InsertWrapper(base.DatabaseOperationWrapper, abc.ABC):

    def __init__(self, conn: connection.DatabaseAdapter, query_builder: query.QueryBuilder, log_filename="log"):
        super(InsertWrapper, self).__init__(conn=conn, query_builder=query_builder, log_filename=log_filename)
        self.conn = conn
        self.query_builder = query_builder

    @abc.abstractmethod
    def insert(self, sensor_data: List[Dict[str, Any]], sensor_id: int = None, sensor_channel: str = None):
        pass
