######################################################
#
# Author: Davide Colombo
# Date: 07/12/21 18:48
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Generator
import airquality.database.repo.repo as baserepo
import airquality.database.conn.adapt as adapt
import airquality.database.util.query as qry
import airquality.types.lookup.lookup as lookuptype
import airquality.types.postgis as pgistype
import airquality.types.line.line as geonametype


class GeoAreaRepo(baserepo.DatabaseRepoABC):

    def __init__(
            self, db_adapter: adapt.DatabaseAdapter, query_builder: qry.QueryBuilder, postgis_cls=pgistype.PostgisPoint
    ):
        super(GeoAreaRepo, self).__init__(db_adapter=db_adapter, query_builder=query_builder)
        self.country_code = None
        self.postgis_cls = postgis_cls

    def with_country_code(self, country_code: str):
        self.country_code = country_code
        return self

    def lookup(self) -> Generator[lookuptype.GeoAreaLookup, None, None]:
        query2exec = self.query_builder.select_geo_area_from_country_code(self.country_code)
        db_lookup = self.db_adapter.send(query2exec)
        for pos, name, country, state, prov, lng, lat in db_lookup:
            yield lookuptype.GeoAreaLookup(
                postal_code=pos, place_name=name, country_code=country, state=state, province=prov, geom=self.postgis_cls(lat=lat, lng=lng)
            )

    def lookup_place_names(self) -> List[str]:
        return [r.place_name for r in self.lookup()]

    def push(self, responses: Generator[geonametype.GeonamesLine, None, None]) -> None:
        geographical_area_values = ','.join(line.line2sql() for line in responses)
        if not geographical_area_values:
            return
        query2exec = self.query_builder.build_initialize_geographical_areas(geographical_area_values)
        self.db_adapter.send(query2exec)
