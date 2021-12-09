######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 20:27
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os

import airquality.logger.util.decorator as log_decorator
import airquality.command.fetch.cmd as command
import airquality.command.basefact as fact
import airquality.file.util.text_parser as fp
import airquality.file.structured.json as file
import airquality.api.fetchwrp as apiwrp
import airquality.api.url.timeiter as urldec
import airquality.api.resp.measure.thingspeak as resp
import airquality.database.repo.measure as dbrepo
import airquality.database.util.query as qry
import airquality.database.conn.adapt as db
import airquality.filter.tsfilt as flt


class ThingspeakFetchFactory(fact.CommandFactory):

    def __init__(self, query_file: file.JSONFile, db_adapt: db.DatabaseAdapter, log_filename="log"):
        super(ThingspeakFetchFactory, self).__init__(query_file=query_file, db_adapt=db_adapt, log_filename=log_filename)

    ################################ create_command ################################
    @log_decorator.log_decorator()
    def get_commands_to_execute(self, command_type: str):

        response_builder, url_time_decorator, fetch_wrapper = self.get_api_side_objects()

        repo = self.get_database_side_objects(sensor_type=command_type)

        response_filter = flt.TimestampFilter(log_filename=self.log_filename)
        response_filter.set_file_logger(self.file_logger)
        response_filter.set_console_logger(self.console_logger)

        cmd = command.FetchCommand(
            time_iterable_url=url_time_decorator,
            fw=fetch_wrapper,
            response_filter=response_filter,
            arb=response_builder,
            db_repo=repo
        )
        cmd.set_file_logger(self.file_logger)
        cmd.set_console_logger(self.console_logger)

        return cmd

    ################################ get_api_side_objects ################################
    @log_decorator.log_decorator()
    def get_api_side_objects(self):
        response_builder = resp.ThingspeakAPIRespBuilder()

        fmt = os.environ['thingspeak_response_fmt']
        url_time_decorator = urldec.ThingspeakTimeIterableURL(url_template=os.environ['thingspeak_url'])
        url_time_decorator.with_url_time_param_template().with_api_response_fmt(fmt)

        response_parser = fp.get_text_parser(file_fmt=fmt, log_filename=self.log_filename)

        fetch_wrapper = apiwrp.FetchWrapper(resp_parser=response_parser, log_filename=self.log_filename)
        fetch_wrapper.set_file_logger(self.file_logger)
        fetch_wrapper.set_console_logger(self.console_logger)

        return response_builder, url_time_decorator, fetch_wrapper

    ################################ get_database_side_objects ################################
    @log_decorator.log_decorator()
    def get_database_side_objects(self, sensor_type: str):
        query_builder = qry.QueryBuilder(query_file=self.query_file)
        return dbrepo.StationMeasureRepo(db_adapter=self.db_adapt, query_builder=query_builder, sensor_type=sensor_type)
