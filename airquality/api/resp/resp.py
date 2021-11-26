######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:39
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, Union


class ParamNameValue:

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


################################ ATMOTUBE API RESPONSE MODEL ################################
class AtmoAPIResp:

    FIELDS = ["voc", "pm1", "pm25", "pm10", "t", "h", "p"]

    def __init__(self, data: Dict[str, Any]):
        self.time = data.get('time')
        self.measures = [ParamNameValue(name=n, value=data.get(n)) for n in AtmoAPIResp.FIELDS]
        self.lat = data.get('coords')['lat']
        self.lon = data.get('coords')['lon']


################################ PURPLEAIR API RESPONSE ################################
class PurpAPIResp:

    CHANNEL_PARAM = [{'name': 'Primary data - Channel A', 'key': 'primary_key_a', 'id': 'primary_id_a'},
                     {'name': 'Primary data - Channel B', 'key': 'primary_key_b', 'id': 'primary_id_b'},
                     {'name': 'Secondary data - Channel A', 'key': 'secondary_key_a', 'id': 'secondary_id_a'},
                     {'name': 'Secondary data - Channel B', 'key': 'secondary_key_b', 'id': 'secondary_id_b'}]

    TYPE = "Purpleair/Thingspeak"

    def __init__(self, data: Dict[str, Any]):
        try:
            self.name = data['name']
            self.sensor_index = data['sensor_index']
            self.latitude = data['latitude']
            self.longitude = data['longitude']
            self.date_created = data['date_created']
            self.data = data
        except KeyError as ke:
            raise SystemExit(f"{PurpAPIResp.__name__}: bad API response => missing key='{ke!s}'")


################################ THINGSPEAK API RESPONSE ################################
class ThnkCH1AResp:
    FIELD_MAP = {"field1": "pm1.0_atm_a", "field2": "pm2.5_atm_a", "field3": "pm10.0_atm_a", "field6": "temperature_a",
                 "field7": "humidity_a"}

    FIELDS = ["pm1.0_atm_a", "pm2.5_atm_a", "pm10.0_atm_a", "temperature_a", "humidity_a"]

    def __init__(self, data: Dict[str, Any]):
        try:
            self.created_at = data['created_at']
            self.measures = [ParamNameValue(name=n, value=data.get(n)) for n in ThnkCH1AResp.FIELDS]
        except KeyError as ke:
            raise SystemExit(f"{ThnkCH1AResp.__name__}: bad API response => missing key='{ke!s}'")


class ThnkCH1BResp:
    FIELD_MAP = {"field1": "pm1.0_atm_b", "field2": "pm2.5_atm_b", "field3": "pm10.0_atm_b", "field6": "pressure_b"}

    FIELDS = ["pm1.0_atm_b", "pm2.5_atm_b", "pm10.0_atm_b", "pressure_b"]

    def __init__(self, data: Dict[str, Any]):
        try:
            self.created_at = data['created_at']
            self.measures = [ParamNameValue(name=n, value=data.get(n)) for n in ThnkCH1BResp.FIELDS]
        except KeyError as ke:
            raise SystemExit(f"{ThnkCH1BResp.__name__}: bad API response => missing key='{ke!s}'")


class ThnkCH2AResp:
    FIELD_MAP = {"field1": "0.3_um_count_a", "field2": "0.5_um_count_a", "field3": "1.0_um_count_a",
                 "field4": "2.5_um_count_a", "field5": "5.0_um_count_a", "field6": "10.0_um_count_a"}

    FIELDS = ["0.3_um_count_a", "0.5_um_count_a", "1.0_um_count_a",
              "2.5_um_count_a", "5.0_um_count_a", "10.0_um_count_a"]

    def __init__(self, data: Dict[str, Any]):
        try:
            self.created_at = data['created_at']
            self.measures = [ParamNameValue(name=n, value=data.get(n)) for n in ThnkCH2AResp.FIELDS]
        except KeyError as ke:
            raise SystemExit(f"{ThnkCH2AResp.__name__}: bad API response => missing key='{ke!s}'")


class ThnkCH2BResp:
    FIELD_MAP = {"field1": "0.3_um_count_b", "field2": "0.5_um_count_b", "field3": "1.0_um_count_b",
                 "field4": "2.5_um_count_b", "field5": "5.0_um_count_b", "field6": "10.0_um_count_b"}

    FIELDS = ["0.3_um_count_b", "0.5_um_count_b", "1.0_um_count_b",
              "2.5_um_count_b", "5.0_um_count_b", "10.0_um_count_b"]

    def __init__(self, data: Dict[str, Any]):
        try:
            self.created_at = data['created_at']
            self.measures = [ParamNameValue(name=n, value=data.get(n)) for n in ThnkCH2BResp.FIELDS]
        except KeyError as ke:
            raise SystemExit(f"{ThnkCH2BResp.__name__}: bad API response => missing key='{ke!s}'")


################################ DEFINE UNION TYPES ################################

THNKRESPTYPE = Union[ThnkCH1AResp, ThnkCH1BResp, ThnkCH2AResp, ThnkCH2BResp]
APIRESPTYPE = Union[AtmoAPIResp, PurpAPIResp, THNKRESPTYPE]
