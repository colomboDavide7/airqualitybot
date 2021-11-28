######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 20:27
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.command.fetch.cmd as command
import airquality.command.basefact as fact

import airquality.logger.util.decorator as log_decorator

import airquality.file.util.parser as fp

import airquality.api.fetchwrp as apiwrp
import airquality.api.url.dynurl as dynurl
import airquality.api.url.timedecor as urldec
import airquality.api.resp.measure as resp

import airquality.database.op.ins.measure as ins
import airquality.database.op.sel.measure as sel
import airquality.database.util.query as qry
import airquality.database.rec.measure as rec
import airquality.filter.tsfilt as flt
import airquality.file.structured.json as file
import airquality.database.conn.adapt as db


class ThingspeakFetchFactory(fact.CommandFactory):

    def __init__(self, api_file: file.JSONFile, query_file: file.JSONFile, conn: db.DatabaseAdapter, log_filename="log"):
        super(ThingspeakFetchFactory, self).__init__(api_file=api_file, query_file=query_file, conn=conn, log_filename=log_filename)

    @log_decorator.log_decorator()
    def create_command(self, sensor_type: str):

        ################################ api-side objects ################################
        response_builder = resp.ThingspeakAPIRespBuilder()

        url_builder = self._get_url_builder()
        url_time_decorator = urldec.ThingspeakURLTimeDecorator(to_decorate=url_builder)

        fmt = self.api_file.format
        response_parser = fp.get_file_parser(file_fmt=fmt, log_filename=self.log_filename)

        fetch_wrapper = apiwrp.FetchWrapper(resp_parser=response_parser, log_filename=self.log_filename)
        fetch_wrapper.set_file_logger(self.file_logger)
        fetch_wrapper.set_console_logger(self.console_logger)

        ################################ database-side objects ################################
        query_builder = qry.QueryBuilder(query_file=self.query_file)

        insert_wrapper = ins.StationMeasureInsertWrapper(
            conn=self.database_conn, builder=query_builder, log_filename=self.log_filename
        )
        insert_wrapper.set_file_logger(self.file_logger)
        insert_wrapper.set_console_logger(self.console_logger)

        select_wrapper = sel.StationMeasureSelectWrapper(
            conn=self.database_conn, builder=query_builder, sensor_type=sensor_type, log_filename=self.log_filename
        )

        ################################ api response filter ################################
        response_filter = flt.TimestampFilter(log_filename=self.log_filename)
        response_filter.set_file_logger(self.file_logger)
        response_filter.set_console_logger(self.console_logger)

        ################################ command object ################################
        cmd = command.FetchCommand(
            tud=url_time_decorator,
            ub=url_builder,
            iw=insert_wrapper,
            sw=select_wrapper,
            fw=fetch_wrapper,
            flt=response_filter,
            arb=response_builder,
            rb_cls=rec.StationMeasureRecord
        )
        cmd.set_file_logger(self.file_logger)
        cmd.set_console_logger(self.console_logger)

        return cmd

    def _get_url_builder(self):
        return dynurl.ThingspeakURLBuilder(
            address=self.api_file.address,
            options=self.api_file.options,
            fmt=self.api_file.format
        )
