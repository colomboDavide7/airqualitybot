######################################################
#
# Author: Davide Colombo
# Date: 14/12/21 11:14
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Generator
import airquality.database.repo.abc as sqlabc
import airquality.file.json as filetype
import airquality.database.conn as dbtype
import airquality.file.line.abc as linetype


# ------------------------------- GeoareaDBRepo ------------------------------- #
class GeoareaDBRepo(sqlabc.DBRepoABC):

    def __init__(self, db_adapter: dbtype.DBConnABC, sql_queries: filetype.JSONFile):
        self.db_adapter = db_adapter
        self.sql_queries = sql_queries

    ################################ push() ################################
    def push(self, lines: Generator[linetype.GeoareaLineTypeABC, None, None]) -> None:
        geoarea_values = ""
        for line in lines:
            geoarea_values += f"('{line.postal_code()}', '{line.country_code()}', '{line.place_name()}', " \
                              f"'{line.province()}', '{line.state()}', {line.geolocation().geom_from_text()}),"
        if geoarea_values:
            query2exec = f"{self.sql_queries.i6} {geoarea_values.strip(',')};"
            self.db_adapter.execute(query2exec)
