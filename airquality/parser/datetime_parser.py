#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 12:04
# @Description: this script defines a class for parsing sensor's API timestamps
#
#################################################
import builtins
from typing import Dict, Any


class DatetimeParser(builtins.object):


    @staticmethod
    def parse_atmotube_timestamp(ts: str) -> str:
        if not isinstance(ts, str):
            raise SystemExit(f"{DatetimeParser.__name__}: error while parsing timestamp in method "
                             f"{DatetimeParser.parse_atmotube_timestamp.__name__}: "
                             f"timestamp must be instance of class 'str'")

        if ts == "":
            raise SystemExit(f"{DatetimeParser.__name__}: cannot parse empty timestamp in method "
                             f"{DatetimeParser.parse_atmotube_timestamp.__name__}")

        ts = ts.strip('Z')
        return ts.replace("T", " ")

    @staticmethod
    def last_date_from_api_param(api_param: Dict[str, Any]) -> str:

        if "date" not in api_param.keys():
            raise SystemExit(f"{DatetimeParser.__name__}: missing 'date' key in method "
                             f"{DatetimeParser.last_date_from_api_param.__name__}.")

        date = ""
        if api_param["date"] is not None:
            date, time = api_param["date"].split(" ")
        return date
