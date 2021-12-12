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
import airquality.logger.util.log as log
import airquality.database.conn.adapt as dbadapt
import airquality.database.util.query as qry
import airquality.file.structured.json as jsonfile


class EnvFactory(abc.ABC):

    def __init__(self, path_to_env: str, command_name: str, command_type: str):
        dotenv.load_dotenv(dotenv_path=path_to_env)
        self.command_name = command_name
        self.command_type = command_type

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
        fullpath = f"{self.log_dir}/{self.command_name}/{self.command_type}.log"
        fullname = f"{self.command_type}_{self.command_name}_logger"
        return log.get_file_logger(file_path=fullpath, logger_name=fullname)

    @property
    def error_logger(self) -> log.logging.Logger:
        fullpath = f"{self.log_dir}/errors.log"
        fullname = f"error_logger"
        return log.get_file_logger(file_path=fullpath, logger_name=fullname)

    @property
    def console_logger(self) -> log.logging.Logger:
        return log.get_console_logger(use_color=True)

    @property
    def db_adapter(self) -> dbadapt.DatabaseAdapter:
        connection_string = os.environ['connection']
        db_adapter = dbadapt.Psycopg2DatabaseAdapter(connection_string=connection_string)
        db_adapter.open_conn()
        return db_adapter

    @property
    def query_builder(self) -> qry.QueryBuilder:
        fullpath = f"{self.prop_dir}/{os.environ['query_file']}"
        json_file = jsonfile.JSONFile(path_to_file=fullpath)
        return qry.QueryBuilder(query_file=json_file)
