######################################################
#
# Author: Davide Colombo
# Date: 07/12/21 18:48
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Generator
import airquality.database.repo.abc as repoabc
import airquality.database.adapt as adapt
import airquality.file.json as filetype
import airquality.types.postgis as pgistype


# ------------------------------- GeoareaLookupType ------------------------------- #
class GeoareaLookupType(object):

    def __init__(
            self, postal_code: str, place_name: str, country_code: str, state: str, province: str, geom: pgistype.PostgisGeometry
    ):
        self.postal_code = postal_code
        self.place_name = place_name
        self.country_code = country_code
        self.state = state
        self.province = province
        self.geom = geom


# ------------------------------- GeoareaRepo ------------------------------- #
class GeoareaRepo(repoabc.DatabaseRepoABC):

    def __init__(
            self, db_adapter: adapt.DBAdaptABC, sql_queries: filetype.JSONFile, country_code: str, postgis_cls=pgistype.PostgisPoint
    ):
        super(GeoareaRepo, self).__init__(db_adapter=db_adapter, sql_queries=sql_queries)
        self.country_code = country_code
        self.postgis_cls = postgis_cls

    @property
    def places(self) -> Generator[str, None, None]:
        for lookup in self.lookup():
            yield lookup.place_name

    @property
    def geoarea_query(self) -> str:
        return self.sql_queries.i6

    ################################ lookup() ################################
    def lookup(self) -> Generator[GeoareaLookupType, None, None]:
        query2exec = self.sql_queries.s13.format(cc=self.country_code)
        db_lookup = self.db_adapter.execute(query2exec)
        for pos, name, country, state, prov, lng, lat in db_lookup:
            yield GeoareaLookupType(
                    postal_code=pos, place_name=name, country_code=country, state=state, province=prov, geom=self.postgis_cls(lat=lat, lng=lng)
                )
