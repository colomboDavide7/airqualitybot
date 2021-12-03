######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 16:18
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import airquality.command.initsrv.cmd as cmd
import airquality.command.basefact as fact
import airquality.logger.util.decorator as log_decorator
import airquality.file.util.line_parser as parser
import airquality.file.line.geobuilder as gl
import airquality.filter.linefilt as flt
import airquality.database.op.sel.geoarea as geosel
import airquality.database.conn.adapt as db
import airquality.database.util.query as qry
import airquality.file.structured.json as file


class InitServiceCommandFactory(fact.CommandFactory):

    def __init__(self, query_file: file.JSONFile, conn: db.DatabaseAdapter, log_filename="log"):
        super(InitServiceCommandFactory, self).__init__(query_file=query_file, conn=conn, log_filename=log_filename)

    @log_decorator.log_decorator()
    def create_command(self, sensor_type: str):
        path_to_geonames_directory = f"{os.environ['directory_of_resources']}/{sensor_type}"
        line_parser, line_builder = self.get_api_side_objects()

        line_filter = flt.LineFilter(log_filename=self.log_filename)
        line_filter.set_file_logger(self.file_logger)
        line_filter.set_console_logger(self.console_logger)

        select_wrapper = self.get_database_side_objects(sensor_type)

        command = cmd.ServiceInitCommand(
            p2g=path_to_geonames_directory,
            lp=line_parser,
            lb=line_builder,
            lf=line_filter,
            gsw=select_wrapper,
            log_filename=self.log_filename
        )
        command.set_console_logger(self.console_logger)
        command.set_file_logger(self.file_logger)
        return command

    def get_api_side_objects(self):
        line_parser = parser.get_line_parser("\t", log_filename=self.log_filename)
        line_builder = gl.GeonamesLineBuilder(log_filename=self.log_filename)
        return line_parser, line_builder

    def get_database_side_objects(self, sensor_type: str):
        query_builder = qry.QueryBuilder(self.query_file)

        select_wrapper = geosel.GeographicSelectWrapper(
            conn=self.database_conn, query_builder=query_builder, log_filename=self.log_filename
        )

        return select_wrapper
