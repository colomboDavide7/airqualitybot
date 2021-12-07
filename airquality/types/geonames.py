######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 17:04
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.types.postgis as pgistype


class GeonamesLine:

    def __init__(self, postal_code: str, place_name: str, country_code: str, province: str, state: str, geom: pgistype.PostgisPoint):
        self.postal_code = postal_code
        self.place_name = place_name.replace("'", " ")
        self.country_code = country_code
        self.province = province.replace("'", " ")
        self.state = state.replace("'", " ")
        self.geom = geom

    def line2sql(self) -> str:
        return f"('{self.postal_code}', '{self.country_code}', '{self.place_name}', '{self.province}', '{self.state}', {self.geom.geom_from_text()})"
