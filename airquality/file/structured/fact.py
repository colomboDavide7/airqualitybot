######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 10:14
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict, Any
import airquality.file.structured.json as jf


def get_structured_file(
        file_fmt: str, parsed_content: Dict[str, Any], path_to_object: List[str] = (), log_filename="log"
) -> jf.file.StructuredFile:
    if file_fmt == 'json':
        return jf.JSONFile(parsed_content=parsed_content, path_to_object=path_to_object, log_filename=log_filename)
    else:
        raise SystemExit(f"'{get_structured_file.__name__}()': bad 'file_type'={file_fmt}")
