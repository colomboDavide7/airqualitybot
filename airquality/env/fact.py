######################################################
#
# Author: Davide Colombo
# Date: 11/12/21 17:35
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import abc
import dotenv
import airquality.env.abc as envtype
import airquality.logger.fact as log
import airquality.database.adapt as dbadapt
import airquality.file.json as jsonfile


# ------------------------------- EnvFactABC ------------------------------- #
class EnvFactABC(abc.ABC):

    def __init__(self, path_to_env: str, command: str, target: str):
        dotenv.load_dotenv(dotenv_path=path_to_env)
        self.command = command
        self.target = target
        self._db_adapter = None
        self._sql_queries = None
        self._file_logger = None
        self._console_logger = None
        self._error_logger = None

    @abc.abstractmethod
    def craft_env(self) -> envtype.EnvironmentABC:
        pass

    @property
    def db_conn(self) -> str:
        return os.environ['connection']

    @property
    def log_dir(self) -> str:
        return os.environ['directory_of_logs']

    @property
    def prop_dir(self) -> str:
        return os.environ['directory_of_resources']

    @property
    def file_logger(self) -> log.logging.Logger:
        if self._file_logger is None:
            fullpath = f"{self.log_dir}/{self.command}/{self.target}.log"
            fullname = f"{self.target}_{self.command}_logger"
            self._file_logger = log.get_file_logger(file_path=fullpath, logger_name=fullname, level=log.logging.DEBUG)
        return self._file_logger

    @property
    def error_logger(self) -> log.logging.Logger:
        if self._error_logger is None:
            fullpath = f"{self.log_dir}/errors.log"
            fullname = f"error_logger"
            self._error_logger = log.get_file_logger(file_path=fullpath, logger_name=fullname, level=log.logging.ERROR)
        return self._error_logger

    @property
    def console_logger(self) -> log.logging.Logger:
        if self._console_logger is None:
            self._console_logger = log.get_console_logger(use_color=True, level=log.logging.DEBUG)
        return self._console_logger

    @property
    def db_adapter(self) -> dbadapt.DBAdaptABC:
        if self._db_adapter is None:
            connection_string = os.environ['connection']
            self._db_adapter = dbadapt.Psycopg2DBAdapt(connection_string=connection_string)
        return self._db_adapter

    @property
    def sql_queries(self) -> jsonfile.JSONFile:
        if self._sql_queries is None:
            fullpath = f"{self.prop_dir}/{os.environ['query_file']}"
            self._sql_queries = jsonfile.JSONFile(path_to_file=fullpath)
        return self._sql_queries
