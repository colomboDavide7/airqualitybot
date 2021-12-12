######################################################
#
# Author: Davide Colombo
# Date: 06/12/21 19:10
# Description: INSERT HERE THE DESCRIPTION
#
######################################################


################################ SENSOR MEASURE LOOKUP ###############################
class GeoareaLookup(object):

    def __init__(
            self, postal_code: str, place_name: str, country_code: str, state: str, province: str, geom: pgistype.PostgisGeometry
    ):
        self.postal_code = postal_code
        self.place_name = place_name
        self.country_code = country_code
        self.state = state
        self.province = province
        self.geom = geom
