######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 20:26
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import airquality.logger.util.decorator as log_decorator
import airquality.command.basefact as fact
import airquality.command.fetch.cmd as cmd
import airquality.file.structured.json as file
import airquality.file.util.text_parser as fp
import airquality.api.url.timeiter as urldec
import airquality.api.resp.measure.atmotube as resp
import airquality.database.repo.measure as dbrepo
import airquality.database.conn.adapt as db
import airquality.database.util.query as qry
import airquality.filter.tsfilt as flt
import airquality.types.timestamp as tstype
import airquality.source.api as apisource


################################ ATMOTUBE FETCH COMMAND FACTORY ################################
class AtmotubeFetchFactory(fact.CommandFactory):

    def __init__(self, query_file: file.JSONFile, conn: db.DatabaseAdapter, log_filename="log"):
        super(AtmotubeFetchFactory, self).__init__(query_file=query_file, conn=conn, log_filename=log_filename)

    ################################ create_command ################################
    @log_decorator.log_decorator()
    def create_command(self, sensor_type: str):
        commands_to_execute = []
        db_repo = self.get_database_side_objects(sensor_type=sensor_type)

        fmt = os.environ['atmotube_response_fmt']
        url_template = os.environ['atmotube_url']
        response_parser = fp.get_text_parser(file_fmt=fmt, log_filename=self.log_filename)

        db_lookup = db_repo.lookup()
        for lookup in db_lookup:
            for channel in lookup.channels:

                # Create a fresh new time iterable URL
                time_iterable_url = urldec.AtmotubeTimeIterableURL(url_template)
                time_iterable_url.with_url_time_param_template().with_api_response_fmt(fmt)
                time_iterable_url.with_api_key(channel.ch_key).with_identifier(channel.ch_id)
                time_iterable_url.from_(channel.last_acquisition).to_(tstype.CurrentTimestamp())

                response_builder = resp.AtmotubeAPIRespBuilder().with_channel_name(channel.ch_name)

                api_source = apisource.AtmotubeAPISource(url=time_iterable_url, parser=response_parser, builder=response_builder)

                # Create a fresh new Time filter for filtering
                response_filter = flt.TimestampFilter(log_filename=self.log_filename)
                response_filter.set_filter_ts(channel.last_acquisition)
                response_filter.set_file_logger(self.file_logger)
                response_filter.set_console_logger(self.console_logger)

                # Create a fresh new repository for pushing
                push_repo = self.get_database_side_objects(sensor_type)
                push_repo.push_to(sensor_id=lookup.sensor_id, channel_name=channel.ch_name)

                command = cmd.FetchCommand(
                    api_source=api_source,
                    response_filter=response_filter,
                    db_repo=push_repo
                )
                command.set_file_logger(self.file_logger)
                command.set_console_logger(self.console_logger)
                commands_to_execute.append(command)
        return commands_to_execute

    ################################ get_api_side_objects ################################
    @log_decorator.log_decorator()
    def get_api_side_objects(self):
        pass

    ################################ get_database_side_objects ################################
    @log_decorator.log_decorator()
    def get_database_side_objects(self, sensor_type: str):
        query_builder = qry.QueryBuilder(query_file=self.query_file)
        return dbrepo.MobileMeasureRepo(db_adapter=self.database_conn, query_builder=query_builder, sensor_type=sensor_type)
