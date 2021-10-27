#################################################
#
# @Author: davidecolombo
# @Date: mer, 27-10-2021, 09:03
# @Description: this script defines the classes for picking parameters from json file by passing a list of
#               'keys-to-the-value' path

#               EXAMPLE: if there is a field in json file called 'key1' which inside contains another json object
#               called 'key2':
#               { "key1": { "key2-1": "val1", "key2-2": "val2" } }
#               to extract the parameter associated to the 'key2-2' you have to pass a list of the form: ["key1", "key2-2"]
#
#               The value returned can be any of the JSON object: list, string, bool, none, number
#
#################################################
import builtins
from typing import Dict, Any, List
from airquality.constants.shared_constants import EMPTY_DICT, EMPTY_LIST


class JSONParamPicker(builtins.object):


    @classmethod
    def pick_parameter(cls, parsed_json: Dict[str, Any], path2key: List[str]) -> Any:

        if parsed_json == EMPTY_DICT:
            raise SystemExit(f"{JSONParamPicker.__name__}: cannot pick parameter when 'parsed_json' argument is emtpy.")

        if path2key == EMPTY_LIST:
            raise SystemExit(f"{JSONParamPicker.__name__}: cannot pick parameter when 'path2key' argument is emtpy.")

        # pop the first key
        first_key = path2key.pop(0)
        if first_key not in parsed_json.keys():
            raise SystemExit(f"{JSONParamPicker.__name__}: cannot pick value corresponding to key='{first_key}'.")
        value = parsed_json[first_key]

        # Recursive search
        for key in path2key:
            if key not in value.keys():
                raise SystemExit(f"{JSONParamPicker.__name__}: cannot pick value corresponding to key='{key}'.")
            value = value[key]

        return value
