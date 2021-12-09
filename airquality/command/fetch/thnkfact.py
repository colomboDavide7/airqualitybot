######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 20:27
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
from typing import List
import airquality.logger.util.decorator as log_decorator
import airquality.command.fetch.cmd as cmd
import airquality.command.basefact as cmdfact
import airquality.file.util.text_parser as textparser
import airquality.file.structured.json as jsonfile
import source.api.url.timeiter as iterurl
import source.api.resp.thingspeak as apiresp
import airquality.database.repo.measure as dbrepo
import airquality.database.util.query as qry
import airquality.database.conn.adapt as dbadapt
import airquality.filter.tsfilt as timefilter
import airquality.source.api as apisource
import airquality.types.channel as chtype
import airquality.types.timestamp as tstype


class ThingspeakFetchFactory(cmdfact.CommandFactory):

    def __init__(self, query_file: jsonfile.JSONFile, db_adapt: dbadapt.DatabaseAdapter, log_filename="log"):
        super(ThingspeakFetchFactory, self).__init__(query_file=query_file, db_adapt=db_adapt, log_filename=log_filename)

    ################################ get_commands_to_execute() ################################
    @log_decorator.log_decorator()
    def get_commands_to_execute(self, command_type: str) -> List[cmd.FetchCommand]:

        query_builder = qry.QueryBuilder(query_file=self.query_file)
        lookup_repo = dbrepo.StationMeasureRepo(db_adapter=self.db_adapt, query_builder=query_builder, sensor_type=command_type)

        fmt = os.environ['thingspeak_response_fmt']
        url_template = os.environ['thingspeak_url']
        response_parser = textparser.get_text_parser(file_fmt=fmt, log_filename=self.log_filename)

        db_lookup = lookup_repo.lookup()

        commands_to_execute = []
        for lookup in db_lookup:
            for channel in lookup.channels:
                response_filter = self.craft_response_filter(filter_timestamp=channel.last_acquisition)
                api_source = self.craft_api_source(
                    url_template=url_template, resp_fmt=fmt, channel=channel, response_parser=response_parser
                )
                push_repo = self.craft_database_repo(
                    sensor_type=command_type, query_builder=query_builder, sensor_id=lookup.sensor_id, ch_name=channel.ch_name
                )
                command = self.craft_command(api_source=api_source, response_filter=response_filter, db_repo=push_repo)
                commands_to_execute.append(command)

        tot = len(commands_to_execute)
        self.log_info(f"{self.__class__.__name__} create {tot}/{tot} commands to execute")
        return commands_to_execute

    ################################ craft_command() ################################
    @log_decorator.log_decorator()
    def craft_command(
            self, api_source: apisource.ThingspeakAPISource, response_filter: timefilter.TimestampFilter, db_repo: dbrepo.StationMeasureRepo
    ) -> cmd.FetchCommand:
        command = cmd.FetchCommand(
            api_source=api_source, response_filter=response_filter, db_repo=db_repo, log_filename=self.log_filename
        )
        command.set_file_logger(self.file_logger)
        command.set_console_logger(self.console_logger)
        return command

    ################################ craft_api_source() ################################
    @log_decorator.log_decorator()
    def craft_api_source(
            self, url_template: str, resp_fmt: str, channel: chtype.Channel, response_parser: textparser.TextParser
    ) -> apisource.ThingspeakAPISource:
        time_iterable_url = iterurl.ThingspeakTimeIterableURL(url_template=url_template)
        time_iterable_url.with_url_time_param_template().with_api_response_fmt(fmt=resp_fmt)
        time_iterable_url.with_api_key(api_key=channel.ch_key).with_identifier(ident=channel.ch_id)
        time_iterable_url.from_(start=channel.last_acquisition).to_(stop=tstype.CurrentTimestamp())
        response_builder = apiresp.ThingspeakAPIRespBuilder().with_channel_name(channel_name=channel.ch_name)
        return apisource.ThingspeakAPISource(url=time_iterable_url, parser=response_parser, builder=response_builder)

    ################################ craft_response_filter() ################################
    @log_decorator.log_decorator()
    def craft_response_filter(self, filter_timestamp: tstype.SQLTimestamp) -> timefilter.TimestampFilter:
        response_filter = timefilter.TimestampFilter(log_filename=self.log_filename)
        response_filter.set_filter_ts(filter_timestamp)
        response_filter.set_file_logger(self.file_logger)
        response_filter.set_console_logger(self.console_logger)
        return response_filter

    ################################ craft_database_repo() ################################
    @log_decorator.log_decorator()
    def craft_database_repo(
            self, sensor_type: str, query_builder: qry.QueryBuilder, sensor_id: int, ch_name: str
    ) -> dbrepo.StationMeasureRepo:
        db_repo = dbrepo.StationMeasureRepo(db_adapter=self.db_adapt, query_builder=query_builder, sensor_type=sensor_type)
        db_repo.push_to(sensor_id=sensor_id, channel_name=ch_name)
        return db_repo
