######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 11:18
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import cmd
from typing import Tuple, Dict, Any
import airquality.command.config as cmd_const
import airquality.file.structured.json as jf
import airquality.api.fetch as fetch
import airquality.file.util.parser as fp
import airquality.api.util.extractor as extr
import airquality.api.util.url as url
import airquality.database.util.conn as db_conn
import airquality.logger.loggable as log


class CommandSetup(log.Loggable, abc.ABC):

    def __init__(self, log_filename="log"):
        super(CommandSetup, self).__init__(log_filename=log_filename)

    @abc.abstractmethod
    def setup(self, sensor_type: str):
        pass


################################ get_api_parameters ################################
def get_api_parameters(sensor_type: str, file_path=cmd_const.API_FILE_PATH, log_filename="log") -> Tuple[str, Dict[str, Any]]:

    api_file_obj = load_file(file_path=file_path, path_to_object=[sensor_type], log_filename=log_filename)
    return api_file_obj.api_address, api_file_obj.url_param


################################ load_file ################################
def load_file(file_path: str, path_to_object=(), log_filename="log"):
    file_fmt = file_path.split('.')[-1]  # get the file format
    file_obj = jf.get_file_object_from_file_type(file_type=file_fmt,  # get FileObject object
                                                 file_path=file_path,
                                                 path_to_object=path_to_object,
                                                 log_filename=log_filename)
    file_obj.load()  # load the file content
    return file_obj


################################ open_database_connection ################################
def open_database_connection(connection_string: str, log_filename="log"):
    conn = db_conn.get_database_adapter(connection_string=connection_string, log_filename=log_filename)
    conn.open_conn()
    return conn


################################ get_fetch_wrapper ################################
def get_fetch_wrapper(
        url_builder: url.URLBuilder,
        api_resp_parser: fp.TextParser,
        api_data_extractor: extr.SensorDataExtractor,
        log_filename="log"
) -> fetch.FetchWrapper:
    return fetch.FetchWrapper(url_builder=url_builder,
                              extractor=api_data_extractor,
                              parser=api_resp_parser,
                              log_filename=log_filename)
