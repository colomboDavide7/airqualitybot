######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 11:18
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.logger.loggable as log
import airquality.database.conn.adapt as db
import airquality.file.structured.json as file


class CommandFactory(log.Loggable, abc.ABC):

    def __init__(self, query_file: file.JSONFile, conn: db.DatabaseAdapter, log_filename="log"):
        super(CommandFactory, self).__init__(log_filename=log_filename)
        self.query_file = query_file
        self.database_conn = conn

    @abc.abstractmethod
    def create_command(self, sensor_type: str):
        pass

    @abc.abstractmethod
    def get_api_side_objects(self):
        pass

    @abc.abstractmethod
    def get_database_side_objects(self, sensor_type: str):
        pass
