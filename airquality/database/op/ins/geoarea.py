######################################################
#
# Author: Davide Colombo
# Date: 04/12/21 15:15
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.logger.util.decorator as log_decorator
import airquality.database.op.baseop as base
import airquality.database.conn.adapt as adapt
import airquality.database.util.query as qry
import airquality.types.geonames as gntypes


class GeographicalAreaInsertWrapper(base.DatabaseWrapper):

    def __init__(self, conn: adapt.DatabaseAdapter, query_builder: qry.QueryBuilder, log_filename="log"):
        super(GeographicalAreaInsertWrapper, self).__init__(conn=conn, builder=query_builder, log_filename=log_filename)

    @log_decorator.log_decorator()
    def insert(self, geolines: List[gntypes.GeonamesLine]) -> None:

        geographical_area_values = ','.join(line.line2sql() for line in geolines)
        exec_query = self.query_builder.build_initialize_geographical_areas(geographical_area_values)
        self.database_conn.send(exec_query)
        n = len(geolines)
        self.log_info(f"{GeographicalAreaInsertWrapper.__name__}: inserted {n}/{n} new places")
