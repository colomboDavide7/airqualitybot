######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import airquality.logger.util.decorator as log_decorator
import airquality.command.basefact as fact
import airquality.command.update.cmd as cmd
import airquality.file.util.text_parser as fp
import airquality.file.structured.json as file
import airquality.api.url.public as url
import airquality.api.resp.info.purpleair as resp
import airquality.database.repo.geolocation as dbrepo
import airquality.database.util.query as qry
import airquality.database.conn.adapt as db
import airquality.filter.geolocation as flt
import airquality.source.api as apisource


################################ get_update_command_factory_cls ################################
def get_update_factory_cls(command_type: str) -> fact.CommandFactory.__class__:
    function_name = get_update_factory_cls.__name__
    valid_types = ["purpleair"]

    if command_type == 'purpleair':
        return PurpleairUpdateFactory
    else:
        raise SystemExit(f"{function_name}: bad type => VALID TYPES: [{'|'.join(t for t in valid_types)}]")


################################ PURPLEAIR UPDATE COMMAND FACTORY ################################
class PurpleairUpdateFactory(fact.CommandFactory):

    def __init__(self, query_file: file.JSONFile, db_adapt: db.DatabaseAdapter, log_filename="log"):
        super(PurpleairUpdateFactory, self).__init__(query_file=query_file, db_adapt=db_adapt, log_filename=log_filename)

    ################################ create_command ################################
    @log_decorator.log_decorator()
    def get_commands_to_execute(self, command_type: str):

        api_source = self.get_api_side_objects()
        db_repo = self.get_database_side_objects(sensor_type=command_type)

        response_filter = flt.GeoFilter()
        response_filter.with_database_locations(db_repo.lookup_locations())
        response_filter.set_file_logger(self.file_logger)
        response_filter.set_console_logger(self.console_logger)

        command = cmd.UpdateCommand(
            api_source=api_source,
            db_repo=db_repo,
            response_filter=response_filter,
            log_filename=self.log_filename
        )
        command.set_file_logger(self.file_logger)
        command.set_console_logger(self.console_logger)

        return [command]

    ################################ get_api_side_objects ################################
    @log_decorator.log_decorator()
    def get_api_side_objects(self):
        response_builder = resp.PurpleairAPIRespBuilder()
        url_builder = url.PurpleairURLBuilder(url_template=os.environ['purpleair_url'])
        response_parser = fp.JSONParser(log_filename=self.log_filename)
        return apisource.PurpleairAPISource(url=url_builder, parser=response_parser, builder=response_builder)

    ################################ get_database_side_objects ################################
    @log_decorator.log_decorator()
    def get_database_side_objects(self, sensor_type: str):
        query_builder = qry.QueryBuilder(query_file=self.query_file)
        repo = dbrepo.SensorGeoRepository(db_adapter=self.db_adapt, query_builder=query_builder, sensor_type=sensor_type)
        return repo
