######################################################
#
# Author: Davide Colombo
# Date: 12/12/21 19:42
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.env.sensor.fact as factabc
import airquality.env.env as envtype
import airquality.api.url.deprecated_url as urltype
import airquality.api.url.private as prvturl
import airquality.api.deprecated_repo as apirepo
import airquality.file.parser.json_parser as parser
import airquality.api.resp.thingspeak as builder
import airquality.filter.timestflt as filtertype
import airquality.command.sensor as cmdtype
import airquality.types.timest as tstype
import airquality.database.repo.measure as sqltype


# ------------------------------- ThingspeakEnvFact ------------------------------- #
class ThingspeakEnvFact(factabc.APIEnvFactABC):

    def __init__(self, path_to_env: str, command: str, target: str):
        super(ThingspeakEnvFact, self).__init__(path_to_env=path_to_env, command=command, target=target)

    ################################ craft_env() ################################
    def craft_env(self) -> envtype.Environment:
        url = self.url
        fmt = self.fmt
        resp_parser = parser.JSONParser()

        commands = []
        for api_param in super().api_param:
            private_url = prvturl.PrivateURLFormatter(url_template=url, api_key=api_param.apikey, api_ident=api_param.ident, api_response_fmt=fmt)
            url_builder = urltype.ThingspeakTimeIterableURLFormatter(url=private_url, from_=api_param.last_timest, to_=tstype.CurrentSQLTimest())
            url_builder.set_console_logger(self.console_logger)
            url_builder.set_file_logger(self.file_logger)

            api_repo = apirepo.APIRepo(url_builder=url_builder)
            resp_builder = builder.ThingspeakAPIRespBuilder(channel_name=api_param.name)

            resp_filter = filtertype.TimestFilter(timest_boundary=api_param.last_timest)
            resp_filter.set_file_logger(self.file_logger)
            resp_filter.set_console_logger(self.console_logger)

            measure_param = super().measure_param
            db_repo = sqltype.StationMeasureDBRepo(
                sensor_id=api_param.sensor_id, channel_name=api_param.name, measure_param=measure_param, db_adapter=self.db_conn, sql_queries=self.sql_queries
            )

            command = cmdtype.SensorCommand(
                api_repo=api_repo, resp_parser=resp_parser, resp_builder=resp_builder, resp_filter=resp_filter, db_repo=db_repo
            )
            command.set_file_logger(self.file_logger)
            command.set_console_logger(self.console_logger)

            commands.append(command)

        return envtype.Environment(
            file_logger=self.file_logger,
            console_logger=self.console_logger,
            error_logger=self.error_logger,
            commands=commands
        )
