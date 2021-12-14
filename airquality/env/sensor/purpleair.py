######################################################
#
# Author: Davide Colombo
# Date: 11/12/21 17:32
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.env.sensor.fact as factabc
import airquality.file.json as filetype
import airquality.env.env as envtype
import airquality.api.api_repo as apirepo
import airquality.api.url.purpleair as urltype
import airquality.file.parser.json_parser as parser
import airquality.api.resp.purpleair as builder
import airquality.filter.namefilt as nameflt
import airquality.filter.geolocation as geoflt
import airquality.database.repo.info as inforepo
import airquality.database.repo.geolocation as georepo
import airquality.command.sensor as cmdtype
import airquality.database.sql.info as sqlinfo
import airquality.database.sql.geolocation as sqlgeo


# ------------------------------- PurpleairEnvFact ------------------------------- #
class PurpleairEnvFact(factabc.APIEnvFactABC):

    def __init__(self, path_to_env: str, command: str, target: str):
        super(PurpleairEnvFact, self).__init__(path_to_env=path_to_env, command=command, target=target)

    ################################ craft_env() ################################
    def craft_env(self) -> envtype.Environment:
        file_logger = self.file_logger
        console_logger = self.console_logger

        sql_queries = self.sql_queries

        url_builder = urltype.PurpleairURLBuilder(url=self.url)
        api_repo = apirepo.APIRepo(url_builder=url_builder)
        resp_parser = parser.JSONParser()
        resp_builder = builder.PurpleairAPIRespBuilder()

        db_repo, resp_filter, sql_builder = self.craft_dependencies(sql_queries=sql_queries)
        resp_filter.set_file_logger(file_logger)
        resp_filter.set_console_logger(console_logger)

        command = cmdtype.SensorCommand(
            api_repo=api_repo, resp_parser=resp_parser, resp_builder=resp_builder, resp_filter=resp_filter, sql_builder=sql_builder, db_adapt=self.db_adapter
        )
        command.set_file_logger(file_logger)
        command.set_console_logger(console_logger)

        return envtype.Environment(
            file_logger=file_logger,
            console_logger=console_logger,
            error_logger=self.error_logger,
            commands=[command]
        )

    ################################ craft_dependencies() ################################
    def craft_dependencies(self, sql_queries: filetype.JSONFile):
        if self.command == 'init':
            db_repo = inforepo.SensorInfoRepo(db_adapter=self.db_adapter, sql_queries=sql_queries, sensor_type=self.target)
            resp_filter = nameflt.NameFilter(names=db_repo.database_sensor_names)
            sql_builder = sqlinfo.InfoSQLBuilder(start_id=db_repo.max_sensor_id, sql_queries=sql_queries)
        elif self.command == 'update':
            db_repo = georepo.SensorGeoRepo(db_adapter=self.db_adapter, sql_queries=sql_queries, sensor_type=self.target)
            resp_filter = geoflt.GeoFilter(locations=db_repo.database_locations)
            sql_builder = sqlgeo.GeolocationSQLBuilder(sensor_name2id=db_repo.name2id, sql_queries=sql_queries)
        else:
            raise SystemExit(f"{self.__class__.__name__} in {self.craft_dependencies.__name__}: invalid command "
                             f"'{self.command}' for PurpleAir sensors")
        return db_repo, resp_filter, sql_builder
