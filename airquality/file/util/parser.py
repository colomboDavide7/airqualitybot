#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 10:24
# @Description: this script defines the classes for parsing file content from different extensions.
#
#################################################
import abc
import json
from typing import Dict, Any
import airquality.logger.loggable as log
import airquality.logger.util.decorator as log_decorator


def get_text_parser(file_ext: str, log_filename="app"):

    if file_ext == 'json':
        return JSONParser(log_filename=log_filename)
    else:
        raise SystemExit(f"'{get_text_parser.__name__}()': bad file extension => '{file_ext}' is not supported")


class TextParser(log.Loggable):

    def __init__(self, log_filename="app"):
        super(TextParser, self).__init__(log_filename=log_filename)

    @abc.abstractmethod
    def parse(self, text: str) -> Dict[str, Any]:
        pass


class JSONParser(TextParser):

    def __init__(self, log_filename="app"):
        super(JSONParser, self).__init__(log_filename=log_filename)

    @log_decorator.log_decorator()
    def parse(self, text: str) -> Dict[str, Any]:
        try:
            self.log_info(f"{JSONParser.__name__} try to parse json text...")
            parsed_text = json.loads(text)
            self.log_info(f"{JSONParser.__name__}: done")
            return parsed_text
        except json.decoder.JSONDecodeError as je:
            raise SystemExit(f"{JSONParser.__name__}: bad json schema => {je!s}")
