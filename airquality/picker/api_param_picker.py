#################################################
#
# @Author: davidecolombo
# @Date: mer, 27-10-2021, 11:19
# @Description: this script defines the classes for picking api parameters selected from the database
#
#################################################
import builtins
from typing import Dict, Any, List
from airquality.constants.shared_constants import EMPTY_DICT, EMPTY_LIST



class APIParamPickerPurpleair(builtins.object):


    @classmethod
    def pick_param(cls, api_param: Dict[str, Any], param2pick: List[str]) -> Dict[str, Any]:

        if api_param == EMPTY_DICT:
            raise SystemExit(f"{APIParamPickerPurpleair.__name__}: cannot pick parameters when api param is empty.")

        if param2pick == EMPTY_LIST:
            return api_param

        keys = api_param.keys()
        picked = {}
        for param in param2pick:
            if param not in keys:
                raise SystemExit(f"{APIParamPickerPurpleair.__name__}: param = '{param}' is missing.")
            picked[param] = api_param[param]
        return picked
