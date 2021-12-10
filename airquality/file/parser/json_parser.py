######################################################
#
# Author: Davide Colombo
# Date: 10/12/21 16:32
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import json
from json.decoder import JSONDecodeError
from typing import Dict, Any
import airquality.file.parser.abc as parserabc


class JSONParser(parserabc.FileParserABC):

    def parse(self, text: str) -> Dict[str, Any]:
        try:
            return json.loads(text)
        except JSONDecodeError as err:
            raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} exception => {err!r}")
