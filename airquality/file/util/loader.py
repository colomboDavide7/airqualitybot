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
def load_environment_file(path_to_file: str = ".env"):
    mandated_properties = ["connection", "query_file", "directory_of_resources"]
    dotenv.load_dotenv(dotenv_path=path_to_file)

    for p in mandated_properties:
        if p not in os.environ:
            raise SystemExit(f"{load_environment_file.__name__}(): bad '.env' file structure => missing '{p}' property")

    query_file_path = f"{os.environ['directory_of_resources']}/{os.environ['query_file']}"
    return os.environ['connection'], query_file_path


################################ load_structured_file ################################
def load_structured_file(file_path: str, path_to_object=(), log_filename="log") -> file.StructuredFile:

    file_fmt = file_path.split('.')[-1]
    raw_content = read.open_read_close_file(file_path)
    file_parser = parser.get_file_parser(file_fmt=file_fmt, log_filename=log_filename)
    parsed_content = file_parser.parse(raw_content)

    return fact.get_structured_file(
        file_fmt=file_fmt, parsed_content=parsed_content, path_to_object=path_to_object, log_filename=log_filename
    )
