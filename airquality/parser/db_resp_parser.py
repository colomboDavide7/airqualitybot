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
    """
    Class that defines @staticmethods for parsing different
    database responses from psycopg2 module.
    """

    @staticmethod
    def parse_key_val_response(response: List[Tuple[str, Any]]) -> Dict[str, Any]:
        """
        Static method that parses list of key-value tuples into dictionary.

        If list of more-than-two-elements tuples or less-than-two-elements tuples
        are passed, SystemExit exception is raised.
        """

        if not response:
            return {}

        if not isinstance(response[0], Tuple) or len(response[0]) != 2:
            raise SystemExit(f"{DatabaseResponseParser.__name__}: "
                             f"error while parsing response in "
                             f"'{DatabaseResponseParser.parse_key_val_response.__name__}()':"
                             f"tuple contains more than 2 elements.")
        parsed = {}
        for t in response:
            parsed[t[0]] = t[1]
        return parsed


    @staticmethod
    def parse_one_field_response(response: List[Tuple[Any]]) -> List[Any]:
        """
        Static method that parses a List of one-element tuple into a list.

        If list of more-than-one-element tuple is passed as argument,
        SystemExit exception is raised.
        """

        if not response:
            return []

        if len(response[0]) > 1:
            raise SystemExit(f"{DatabaseResponseParser.__name__}: "
                             f"error while parsing response in "
                             f"'{DatabaseResponseParser.parse_one_field_response.__name__}()':"
                             f"tuple contains more than 1 element.")

        return [t[0] for t in response]



