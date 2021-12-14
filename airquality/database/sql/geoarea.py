######################################################
#
# Author: Davide Colombo
# Date: 14/12/21 11:14
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Generator
import airquality.database.sql.abc as sqlabc
import airquality.file.json as filetype
import airquality.file.line.abc as linetype


# ------------------------------- GeoareaSQLBuilder ------------------------------- #
class GeoareaSQLBuilder(sqlabc.SQLBuilderABC):

    def __init__(self, sql_queries: filetype.JSONFile):
        self.sql_queries = sql_queries

    ################################ sql() ################################
    def sql(self, lines: Generator[linetype.GeoareaLineTypeABC, None, None]) -> str:
        geoarea_values = ""
        for line in lines:
            geoarea_values += f"('{line.postal_code()}', '{line.country_code()}', '{line.place_name()}', " \
                              f"'{line.province()}', '{line.state()}', {line.geolocation().geom_from_text()}),"
        if geoarea_values:
            return f"{self.sql_queries.i6} {geoarea_values.strip(',')};"
