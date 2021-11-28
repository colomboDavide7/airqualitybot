######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 10:06
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import dotenv
import airquality.file.structured.fact as fact
import airquality.file.structured.file as file
import airquality.file.util.parser as parser
import airquality.file.util.reader as read


################################ load_environment_file ################################
def load_environment_file(file_path: str, sensor_type: str):

    dotenv.load_dotenv(dotenv_path=file_path)

    if 'DBCONN' not in os.environ:
        raise SystemExit(f"'{load_environment_file.__name__}()': bad '.env' file structure => missing 'DBCONN'")

    if sensor_type == 'purpleair':
        if not os.environ.get('PURPLEAIR_KEY1'):
            raise SystemExit(f"'{load_environment_file.__name__}()': bad '.env' file structure => "
                             f"'{sensor_type}' sensor type require 'PURPLEAIR_KEY1'")


################################ load_structured_file ################################
def load_structured_file(file_path: str, path_to_object=(), log_filename="log") -> file.StructuredFile:

    file_fmt = file_path.split('.')[-1]
    raw_content = read.open_read_close_file(file_path)
    file_parser = parser.get_file_parser(file_fmt=file_fmt, log_filename=log_filename)
    parsed_content = file_parser.parse(raw_content)

    return fact.get_structured_file(
        file_fmt=file_fmt, parsed_content=parsed_content, path_to_object=path_to_object, log_filename=log_filename
    )
