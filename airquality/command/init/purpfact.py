######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 11:13
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import airquality.logger.util.decorator as log_decorator
import airquality.command.init.cmd as command
import airquality.command.basefact as fact
import airquality.file.util.text_parser as fp
import airquality.file.structured.json as file
import airquality.api.resp.info.purpleair as resp
import airquality.api.url.public as url
import airquality.database.repo.info as dbrepo
import airquality.database.util.query as qry
import airquality.database.conn.adapt as db
import airquality.filter.namefilt as flt
import airquality.source.api as apisource


################################ PURPLEAIR INIT COMMAND FACTORY ################################
class PurpleairInitFactory(fact.CommandFactory):

    def __init__(self, query_file: file.JSONFile, conn: db.DatabaseAdapter, log_filename="log"):
        super(PurpleairInitFactory, self).__init__(query_file=query_file, conn=conn, log_filename=log_filename)

    ################################ create_command ################################
    @log_decorator.log_decorator()
    def create_command(self, sensor_type: str):

        data_source = self.get_api_side_objects()
        db_repo = self.get_database_side_objects(sensor_type=sensor_type)

        response_filter = flt.NameFilter()
        response_filter.with_database_sensor_names(db_repo.lookup_names())
        response_filter.set_file_logger(self.file_logger)
        response_filter.set_console_logger(self.console_logger)

        cmd = command.InitCommand(
            data_source=data_source,
            db_repo=db_repo,
            response_filter=response_filter,
            log_filename=self.log_filename
        )
        cmd.set_file_logger(self.file_logger)
        cmd.set_console_logger(self.console_logger)

        return [cmd]

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
        return dbrepo.SensorInfoRepository(db_adapter=self.database_conn, query_builder=query_builder, sensor_type=sensor_type)
