######################################################
#
# Author: Davide Colombo
# Date: 18/11/21 08:38
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import dotenv


def load_environment_file(file_path: str, sensor_type: str):

    dotenv.load_dotenv(dotenv_path=file_path)

    if not os.environ.get('DBCONN'):
        raise SystemExit(f"'{load_environment_file.__name__}()': bad '.env' file structure => missing 'DBCONN'")

    if sensor_type == 'purpleair':
        if not os.environ.get('PURPLEAIR_KEY1'):
            raise SystemExit(f"'{load_environment_file.__name__}()': bad '.env' file structure => "
                             f"'{sensor_type}' sensor type require 'PURPLEAIR_KEY1'")
