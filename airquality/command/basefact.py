######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 11:18
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List
import airquality.logger.loggable as log
import airquality.command.basecmd as basecmd
import airquality.database.conn.adapt as dbadapt
import airquality.file.structured.json as jsonfile


class CommandFactory(log.Loggable, abc.ABC):

    def __init__(self, query_file: jsonfile.JSONFile, db_adapt: dbadapt.DatabaseAdapter, log_filename="log"):
        super(CommandFactory, self).__init__(log_filename=log_filename)
        self.query_file = query_file
        self.db_adapt = db_adapt

    @abc.abstractmethod
    def get_commands_to_execute(self, command_type: str) -> List[basecmd.Command]:
        pass
