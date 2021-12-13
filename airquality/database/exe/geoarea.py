######################################################
#
# Author: Davide Colombo
# Date: 12/12/21 20:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Generator
import airquality.database.exe.abc as exetype
import airquality.file.line.abc as linetype
import airquality.database.repo.geoarea as dbtype


# ------------------------------- GeoareaQueryExecutor ------------------------------- #
class GeoareaQueryExecutor(exetype.QueryExecutorABC):

    def __init__(self, db_repo: dbtype.GeoareaRepo):
        self._db_repo = db_repo

    def execute(self, data: Generator[linetype.GeoareaLineTypeABC, None, None]) -> None:
        geoarea_values = self._db_repo.geoarea_query
        for line in data:
            geoarea_values += f"('{line.postal_code()}', '{line.country_code()}', '{line.place_name()}', " \
                              f"'{line.province()}', '{line.state()}', {line.geolocation().geom_from_text()}),"

        if geoarea_values != self._db_repo.geoarea_query:
            query2exec = f"{geoarea_values.strip(',')};"
            self._db_repo.push(query2exec)
