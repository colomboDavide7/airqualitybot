######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 19:28
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.database.op.baseop as base
import airquality.database.conn.adapt as adapt
import airquality.database.util.query as qry


class GeographicSelectWrapper(base.DatabaseWrapper):

    def __init__(self, conn: adapt.DatabaseAdapter, query_builder: qry.QueryBuilder, log_filename="log"):
        super(GeographicSelectWrapper, self).__init__(conn=conn, builder=query_builder, log_filename=log_filename)
        self.country_code = None

    def with_country_code(self, country_code: str):
        self.country_code = country_code

    def select(self):
        exec_query = self.query_builder.select_place_names_from_country_code(self.country_code)
        answer = self.database_conn.send(exec_query)
        return [t[0] for t in answer]
