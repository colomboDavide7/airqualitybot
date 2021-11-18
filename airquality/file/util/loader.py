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

    address = file_object.api_address
    url_param = file_object.url_param

    # file extension for building the TextParser
    file_extension = "json"
    if sensor_type in ('atmotube', 'thingspeak'):
        if not url_param.get('format'):
            raise SystemExit(f"bad 'api.json' file structure => '{sensor_type}' sensor type require 'format' param")
        file_extension = url_param['format']

    return address, url_param, file_extension


def load_environment_file(file_path: str, sensor_type: str):

    dotenv.load_dotenv(dotenv_path=file_path)

    if not os.environ.get('DBCONN'):
        raise SystemExit(f"'{load_environment_file.__name__}()': bad '.env' file structure => missing 'DBCONN'")

    if sensor_type == 'purpleair':
        if not os.environ.get('PURPLEAIR_KEY1'):
            raise SystemExit(f"'{load_environment_file.__name__}()': bad '.env' file structure => "
                             f"'{sensor_type}' sensor type require 'PURPLEAIR_KEY1'")
