######################################################
#
# Author: Davide Colombo
# Date: 18/11/21 08:38
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import dotenv
from typing import Tuple, Dict, Any
import airquality.file.structured.json as jf


def get_api_param_from_file(sensor_type: str, file_object: jf.JSONFile) -> Tuple[str, Dict[str, Any], str]:

    url_param = file_object.url_param

    # 'api_response_format' variable is used to decide which type of TextParser build for parsing API response
    api_response_format = "json"
    if sensor_type in ('atmotube', 'thingspeak'):
        if 'format' not in url_param:
            raise SystemExit(f"'{get_api_param_from_file.__name__}():'bad 'api.json' file structure => "
                             f"'{sensor_type}' sensor type require 'format' param")
        api_response_format = url_param['format']

    return file_object.api_address, url_param, api_response_format


def load_environment_file(file_path: str, sensor_type: str):

    dotenv.load_dotenv(dotenv_path=file_path)

    if not os.environ.get('DBCONN'):
        raise SystemExit(f"'{load_environment_file.__name__}()': bad '.env' file structure => missing 'DBCONN'")

    if sensor_type == 'purpleair':
        if not os.environ.get('PURPLEAIR_KEY1'):
            raise SystemExit(f"'{load_environment_file.__name__}()': bad '.env' file structure => "
                             f"'{sensor_type}' sensor type require 'PURPLEAIR_KEY1'")
