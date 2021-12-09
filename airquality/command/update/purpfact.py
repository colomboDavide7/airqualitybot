######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
from typing import List, Dict
import airquality.logger.util.decorator as log_decorator
import airquality.command.basefact as cmdfact
import airquality.command.update.cmd as cmd
import airquality.file.util.text_parser as textparser
import airquality.file.structured.json as jsonfile
import source.api.url.purpleair as publicurl
import source.api.resp.purpleair as purprespbuilder
import airquality.database.repo.geolocation as dbrepo
import airquality.database.util.query as qry
import airquality.database.conn.adapt as dbadapt
import airquality.filter.geolocation as geolocfilter
import airquality.source.api as apisource


################################ get_update_command_factory_cls ################################
def get_update_factory_cls(command_type: str) -> cmdfact.CommandFactory.__class__:
    function_name = get_update_factory_cls.__name__
    valid_types = ["purpleair"]

    if command_type == 'purpleair':
        return PurpleairUpdateFactory
    else:
        raise SystemExit(f"{function_name}: bad type => VALID TYPES: [{'|'.join(t for t in valid_types)}]")


################################ PURPLEAIR UPDATE COMMAND FACTORY ################################
class PurpleairUpdateFactory(cmdfact.CommandFactory):

    def __init__(self, query_file: jsonfile.JSONFile, db_adapt: dbadapt.DatabaseAdapter, log_filename="log"):
        super(PurpleairUpdateFactory, self).__init__(query_file=query_file, db_adapt=db_adapt, log_filename=log_filename)

    ################################ get_commands_to_execute() ################################
    @log_decorator.log_decorator()
    def get_commands_to_execute(self, command_type: str) -> List[cmd.UpdateCommand]:

        api_source = self.craft_api_source(url_template=os.environ['purpleair_url'])
        db_repo = self.craft_database_repo(command_type=command_type)
        response_filter = self.craft_response_filter(database_locations=db_repo.database_locations)

        command = cmd.UpdateCommand(
            api_source=api_source, db_repo=db_repo, response_filter=response_filter, log_filename=self.log_filename
        )
        command.set_file_logger(self.file_logger)
        command.set_console_logger(self.console_logger)

        return [command]

    ################################ craft_api_source() ################################
    @log_decorator.log_decorator()
    def craft_api_source(self, url_template: str) -> apisource.PurpleairAPISource:
        response_builder = purprespbuilder.PurpleairAPIRespBuilder()
        url_builder = publicurl.PurpleairURLBuilder(url_template)
        response_parser = textparser.JSONParser(log_filename=self.log_filename)
        return apisource.PurpleairAPISource(url=url_builder, parser=response_parser, builder=response_builder)

    ################################ craft_response_filter() ################################
    @log_decorator.log_decorator()
    def craft_response_filter(self, database_locations: Dict[str, str]) -> geolocfilter.GeoFilter:
        response_filter = geolocfilter.GeoFilter()
        response_filter.with_database_locations(database_locations)
        response_filter.set_file_logger(self.file_logger)
        response_filter.set_console_logger(self.console_logger)
        return response_filter

    ################################ craft_database_repo() ################################
    @log_decorator.log_decorator()
    def craft_database_repo(self, command_type: str) -> dbrepo.SensorGeoRepository:
        query_builder = qry.QueryBuilder(query_file=self.query_file)
        repo = dbrepo.SensorGeoRepository(db_adapter=self.db_adapt, query_builder=query_builder, sensor_type=command_type)
        return repo
