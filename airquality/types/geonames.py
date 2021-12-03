######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 17:04
# Description: INSERT HERE THE DESCRIPTION
#
######################################################


class GeonamesLine:

    def __init__(self, postal_code: str, place_name: str, country_code: str, province: str, state: str):
        self.postal_code = postal_code
        self.place_name = place_name
        self.country_code = country_code
        self.province = province
        self.state = state
