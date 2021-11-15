######################################################
#
# Author: Davide Colombo
# Date: 14/11/21 21:59
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.database.util.conn as db
import airquality.database.util.sql.query as query
import airquality.logger.loggable as log


class DatabaseOperationWrapper(log.Loggable):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder):
        super(DatabaseOperationWrapper, self).__init__()
        self.conn = conn
        self.builder = query_builder
