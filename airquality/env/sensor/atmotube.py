######################################################
#
# Author: Davide Colombo
# Date: 12/12/21 10:52
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.env.sensor.fact as factabc
import airquality.env.env as envtype
# import airquality.api.url.timeiter as urltype
import airquality.api.urlfmt as urlfmt
import airquality.api.deprecated_repo as apirepo
import airquality.file.parser.json_parser as parser
import airquality.api.resp.atmotube as builder
import airquality.filter.timestflt as filtertype
import airquality.command.sensor as cmdtype
import airquality.types.timest as tstype
import airquality.database.repo.measure as sqltype


# ------------------------------- AtmotubeEnvFact ------------------------------- #
class AtmotubeEnvFact(factabc.APIEnvFactABC):

    def __init__(self, path_to_env: str, command: str, target: str):
        super(AtmotubeEnvFact, self).__init__(path_to_env=path_to_env, command=command, target=target)

    ################################ craft_env() ################################
    def craft_env(self) -> envtype.Environment:
        resp_parser = parser.JSONParser()

        commands = []
        for sensor_id, channel_key, channel_id, channel_name, last_acquisition_dt in super().api_param:
            timest_boundary = tstype.datetime2sqltimest(last_acquisition_dt)
            formatted_url = self.url.format(api_key=channel_key, api_id=channel_id, api_fmt=self.fmt)
            url_formatter = urlfmt.AtmotubeURLFormatter(url_template=formatted_url)
            # url_formatter = urltype.AtmotubeTimeIterableURLFormatter(url=formatted_url, from_=timest_boundary, to_=tstype.CurrentSQLTimest())

            api_repo = apirepo.APIRepo(url_builder=url_formatter)
            resp_builder = builder.AtmotubeAPIRespBuilder(channel_name=channel_name)

            resp_filter = filtertype.TimestFilter(timest_boundary=timest_boundary)
            resp_filter.set_file_logger(self.file_logger)
            resp_filter.set_console_logger(self.console_logger)

            measure_param = super().measure_param
            db_repo = sqltype.MobileMeasureDBRepo(
                sensor_id=sensor_id, channel_name=channel_name, measure_param=measure_param, db_adapter=self.db_conn, sql_queries=self.sql_queries
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
