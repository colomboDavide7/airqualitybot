# ======================================
# @author:  Davide Colombo
# @date:    2022-02-2, mer, 12:36
# ======================================
from dataclasses import dataclass


class GeonamesDM(object):
    """
    An *object* class that defines the raw datastructure of a geonames country file.
    """

    def __init__(self, *args):
        self.country_code = args[0]                     # The place's 2-alpha ISO country code.
        self.postal_code = args[1]                      # The place's postal code.
        self.place_name = args[2].replace("'", "")      # The place's name.
        self.state = args[3].replace("'", "")           # The place's state extended name.
        self.province = args[5].replace("'", "")        # The place's province extended name.
        self.latitude = float(args[9])                  # The place's latitude in WGS84 System Reference.
        self.longitude = float(args[10])                # The place's longitude in WGS84 System Reference.


@dataclass
class CityDM(object):
    """
    A *dataclass* that defines the raw datastructure for city's data read from file and used for saying to the
    program which city include when downloading weather data.
    """

    country_code: str                                   # The 2-alpha ISO city's country code.
    place_name: str                                     # The city's name.

    def __str__(self):
        return f"{self.place_name}, {self.country_code}"
