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


def get_text_parser(file_ext: str, log_filename="log"):

    if file_ext == 'json':
        return JSONParser(log_filename=log_filename)
    else:
        raise SystemExit(f"'{get_text_parser.__name__}()': bad file extension => '{file_ext}' is not supported")


class TextParser(log.Loggable):

    def __init__(self, log_filename="log"):
        super(TextParser, self).__init__(log_filename=log_filename)

    @abc.abstractmethod
    def parse(self, text: str) -> Dict[str, Any]:
        pass


class JSONParser(TextParser):

    def __init__(self, log_filename="log"):
        super(JSONParser, self).__init__(log_filename=log_filename)

    @log_decorator.log_decorator()
    def parse(self, text: str) -> Dict[str, Any]:
        try:
            parsed_text = json.loads(text)
            return parsed_text
        except json.decoder.JSONDecodeError as je:
            raise SystemExit(f"{JSONParser.__name__}: bad json schema => {je!s}")
