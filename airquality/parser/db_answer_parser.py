#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 11:36
# @Description: this script defines a class for parsing database answers.
#
#################################################
import builtins
from typing import Dict, Any, List, Tuple
from airquality.constants.shared_constants import EMPTY_LIST, EMPTY_DICT


class DatabaseAnswerParser(builtins.object):
    """Class that defines @staticmethods for parsing psycopg2 database answers."""


    @staticmethod
    def parse_key_val_answer(response: List[Tuple[str, Any]]) -> Dict[str, Any]:
        """Static method that parses list of key-value tuples into dictionary.

        If list of more-than-two-elements tuples or less-than-two-elements tuples is passed,
        SystemExit exception is raised."""

        if response == EMPTY_LIST:
            return EMPTY_DICT

        if not isinstance(response[0], Tuple) or len(response[0]) != 2:
            raise SystemExit(f"{DatabaseAnswerParser.__name__}: error while parsing answer in "
                             f"'{DatabaseAnswerParser.parse_key_val_answer.__name__}()':"
                             f"tuple contains more than 2 elements.")
        parsed = {}
        for t in response:
            parsed[t[0]] = t[1]
        return parsed


    @staticmethod
    def parse_single_attribute_answer(response: List[Tuple[Any]]) -> List[Any]:
        """Static method that parses a List of one-element tuple into a list.

        If list of more-than-one-element tuple is passed as argument, SystemExit exception is raised."""

        if response == EMPTY_LIST:
            return EMPTY_LIST

        if len(response[0]) > 1:
            raise SystemExit(f"{DatabaseAnswerParser.__name__}: error while parsing answer in "
                             f"'{DatabaseAnswerParser.parse_single_attribute_answer.__name__}()':"
                             f"tuple contains more than 1 element.")

        return [t[0] for t in response]
