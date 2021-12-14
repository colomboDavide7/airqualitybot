######################################################
#
# Author: Davide Colombo
# Date: 12/12/21 10:52
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.env.sensor.fact as factabc
import airquality.env.env as envtype
import airquality.api.url.timeiter as urltype
import airquality.api.url.private as prvturl
import airquality.api.api_repo as apirepo
import airquality.file.parser.json_parser as parser
import airquality.api.resp.atmotube as builder
import airquality.filter.tsfilt as filtertype
import airquality.command.sensor as cmdtype
import airquality.types.timestamp as tstype
import airquality.database.sql.measure as sqltype


# ------------------------------- AtmotubeEnvFact ------------------------------- #
class AtmotubeEnvFact(factabc.APIEnvFactABC):

    def __init__(self, path_to_env: str, command: str, target: str):
        super(AtmotubeEnvFact, self).__init__(path_to_env=path_to_env, command=command, target=target)

    ################################ craft_env() ################################
    def craft_env(self) -> envtype.Environment:
        url = self.url
        fmt = self.fmt
        resp_parser = parser.JSONParser()

        commands = []
        for api_param in super().api_param:
            private_url = prvturl.PrivateURLBuilder(url=url, key=api_param.ch_key, ident=api_param.ch_id, fmt=fmt)
            url_builder = urltype.AtmotubeTimeIterableURL(url=private_url, from_=api_param.last_acquisition, to_=tstype.CurrentTimestamp())
            url_builder.set_console_logger(self.console_logger)
            url_builder.set_file_logger(self.file_logger)

            api_repo = apirepo.APIRepo(url_builder=url_builder)
            resp_builder = builder.AtmotubeAPIRespBuilder(channel_name=api_param.ch_name)

            resp_filter = filtertype.TimestampFilter(filter_ts=api_param.last_acquisition)
            resp_filter.set_file_logger(self.file_logger)
            resp_filter.set_console_logger(self.console_logger)

            measure_param = super().measure_param
            db_repo = sqltype.MobileMeasureDBRepo(
                sensor_id=api_param.sensor_id, channel_name=api_param.ch_name, measure_param=measure_param, db_adapter=self.db_adapter, sql_queries=self.sql_queries
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
