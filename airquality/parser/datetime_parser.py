#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 12:04
# @Description: this script defines a class for parsing sensor's API timestamps
#
#################################################
import builtins


class DatetimeParser(builtins.object):


    @staticmethod
    def parser_atmotube_timestamp(ts: str) -> str:
        if not isinstance(ts, str):
            raise SystemExit(f"{DatetimeParser.__name__}: error while parsing timestamp in method "
                             f"{DatetimeParser.parser_atmotube_timestamp.__name__}: "
                             f"timestamp must be instance of class 'str'")

        if ts == "":
            raise SystemExit(f"{DatetimeParser.__name__}: cannot parse empty timestamp in method "
                             f"{DatetimeParser.parser_atmotube_timestamp.__name__}")

        ts = ts.strip('Z')
        return ts.replace("T", " ")
