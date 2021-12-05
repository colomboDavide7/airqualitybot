######################################################
#
# Author: Davide Colombo
# Date: 04/12/21 15:15
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Generator
import airquality.logger.util.decorator as log_decorator
import airquality.database.op.baseop as base
import airquality.database.conn.adapt as adapt
import airquality.database.util.query as qry
import airquality.types.geonames as gntypes


class GeographicalAreaInsertWrapper(base.DatabaseWrapper):

    def __init__(self, conn: adapt.DatabaseAdapter, query_builder: qry.QueryBuilder, log_filename="log"):
        super(GeographicalAreaInsertWrapper, self).__init__(conn=conn, builder=query_builder, log_filename=log_filename)

    @log_decorator.log_decorator()
    def insert(self, geolines: Generator[gntypes.GeonamesLine,  None, None]) -> None:

        geographical_area_values = ','.join(line.line2sql() for line in geolines)
        if not geographical_area_values:
            return

        exec_query = self.query_builder.build_initialize_geographical_areas(geographical_area_values)
        self.database_conn.send(exec_query)
