######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 11:13
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
from typing import List
import airquality.logger.util.decorator as log_decorator
import init as command
import airquality.command.basefact as cmdfact
import airquality.file.util.text_parser as textparser
import airquality.file.structured.json as jsonfile
import api as purprespbuilder
import api as publicurl
import airquality.database.repo.info as dbrepo
import airquality.database.util.query as qry
import airquality.database.conn.adapt as dbadapt
import airquality.filter.namefilt as namefilter
import api as apisource


################################ PURPLEAIR INIT COMMAND FACTORY ################################
class PurpleairInitFactory(cmdfact.CommandFactory):

    def __init__(self, query_file: jsonfile.JSONFile, db_adapt: dbadapt.DatabaseAdapter, log_filename="log"):
        super(PurpleairInitFactory, self).__init__(query_file=query_file, db_adapt=db_adapt, log_filename=log_filename)

    ################################ get_commands_to_execute() ################################
    @log_decorator.log_decorator()
    def get_commands_to_execute(self, command_type: str) -> List[command.InitCommand]:
        api_source = self.craft_api_source(url_template=os.environ['purpleair_url'])
        db_repo = self.craft_database_repo(command_type)
        response_filter = self.craft_response_filter(db_repo.database_sensor_names)
        cmd = command.InitCommand(
            api_source=api_source, db_repo=db_repo, response_filter=response_filter, log_filename=self.log_filename
        )
        cmd.set_file_logger(self._file_logger)
        cmd.set_console_logger(self._console_logger)

        return [cmd]

    ################################ craft_api_source() ################################
    @log_decorator.log_decorator()
    def craft_api_source(self, url_template: str) -> apisource.PurpleairAPISource:
        response_builder = purprespbuilder.PurpleairAPIRespBuilder()
        url_builder = publicurl.PurpleairURLBuilder(url_template)
        response_parser = textparser.JSONParser(log_filename=self.log_filename)
        return apisource.PurpleairAPISource(url=url_builder, parser=response_parser, builder=response_builder)

    ################################ craft_response_filter() ################################
    @log_decorator.log_decorator()
    def craft_response_filter(self, database_sensor_names: List[str]) -> namefilter.NameFilter:
        response_filter = namefilter.NameFilter()
        response_filter.with_database_sensor_names(database_sensor_names)
        response_filter.set_file_logger(self._file_logger)
        response_filter.set_console_logger(self._console_logger)
        return response_filter

    ################################ craft_database_repo() ################################
    @log_decorator.log_decorator()
    def craft_database_repo(self, command_type: str):
        query_builder = qry.QueryBuilder(query_file=self.query_file)
        return dbrepo.SensorInfoRepo(db_adapter=self.db_adapt, query_builder=query_builder, sensor_type=command_type)
