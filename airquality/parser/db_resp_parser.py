#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 11:36
# @Description: This script defines the database response parser class and
#               its methods for parsing database responses.
#
#################################################
import builtins
from typing import Dict, Any, List, Tuple


class DatabaseResponseParser(builtins.object):


    @staticmethod
    def parse_key_val_response(response: List[Tuple[str, Any]]) -> Dict[str, Any]:
        """
        Static method that parses list of key-value tuples into dictionary.
        """

        parsed = {}
        if not response:
            return parsed

        if len(response[0]) != 2:
            raise SystemExit(f"{DatabaseResponseParser.__name__}: "
                             f"error while parsing response in "
                             f"'{DatabaseResponseParser.parse_key_val_response.__name__}()':"
                             f"tuple contains more than 2 values.")

        for t in response:
            parsed[t[0]] = t[1]
        return parsed
