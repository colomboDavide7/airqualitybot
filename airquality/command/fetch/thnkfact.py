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
import airquality.api.url.dynurl as dynurl
import airquality.api.url.timedecor as urldec
import airquality.api.resp.measure.thingspeak as resp
import airquality.database.op.ins.measure as ins
import airquality.database.op.sel.measure as sel
import airquality.database.util.query as qry
import airquality.database.rec.measure as rec
import airquality.database.conn.adapt as db
import airquality.filter.tsfilt as flt


class ThingspeakFetchFactory(fact.CommandFactory):

    def __init__(self, query_file: file.JSONFile, conn: db.DatabaseAdapter, log_filename="log"):
        super(ThingspeakFetchFactory, self).__init__(query_file=query_file, conn=conn, log_filename=log_filename)

    ################################ create_command ################################
    @log_decorator.log_decorator()
    def create_command(self, sensor_type: str):

        response_builder, url_builder, url_time_decorator, fetch_wrapper = self.get_api_side_objects()

        insert_wrapper, select_wrapper = self.get_database_side_objects(sensor_type=sensor_type)

        response_filter = flt.TimestampFilter(log_filename=self.log_filename)
        response_filter.set_file_logger(self.file_logger)
        response_filter.set_console_logger(self.console_logger)

        cmd = command.FetchCommand(
            tud=url_time_decorator,
            ub=url_builder,
            iw=insert_wrapper,
            sw=select_wrapper,
            fw=fetch_wrapper,
            flt=response_filter,
            arb=response_builder
        )
        cmd.set_file_logger(self.file_logger)
        cmd.set_console_logger(self.console_logger)

        return cmd

    ################################ get_api_side_objects ################################
    @log_decorator.log_decorator()
    def get_api_side_objects(self):
        response_builder = resp.ThingspeakAPIRespBuilder()

        fmt = os.environ['thingspeak_response_fmt']
        url_builder = dynurl.ThingspeakURLBuilder(url_template=os.environ['thingspeak_url'])
        url_builder.with_api_response_fmt(fmt)
        url_time_decorator = urldec.ThingspeakURLTimeDecorator(to_decorate=url_builder)

        response_parser = fp.get_text_parser(file_fmt=fmt, log_filename=self.log_filename)

        fetch_wrapper = apiwrp.FetchWrapper(resp_parser=response_parser, log_filename=self.log_filename)
        fetch_wrapper.set_file_logger(self.file_logger)
        fetch_wrapper.set_console_logger(self.console_logger)

        return response_builder, url_builder, url_time_decorator, fetch_wrapper

    ################################ get_database_side_objects ################################
    @log_decorator.log_decorator()
    def get_database_side_objects(self, sensor_type: str):
        query_builder = qry.QueryBuilder(query_file=self.query_file)
        record_builder = rec.StationRecordBuilder()

        insert_wrapper = ins.StationInsertWrapper(
            conn=self.database_conn, builder=query_builder, record_builder=record_builder, log_filename=self.log_filename
        )
        insert_wrapper.set_file_logger(self.file_logger)
        insert_wrapper.set_console_logger(self.console_logger)

        select_wrapper = sel.StationMeasureSelectWrapper(
            conn=self.database_conn, builder=query_builder, sensor_type=sensor_type, log_filename=self.log_filename
        )
        return insert_wrapper, select_wrapper
