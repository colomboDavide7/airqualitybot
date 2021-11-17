######################################################
#
# Author: Davide Colombo
# Date: 17/11/21 16:27
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.database.operation.base as base
import airquality.database.util.conn as db
import airquality.database.util.query as query


class UpdateWrapper(base.DatabaseOperationWrapper):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder):
        super(UpdateWrapper, self).__init__(conn=conn, query_builder=query_builder)
    