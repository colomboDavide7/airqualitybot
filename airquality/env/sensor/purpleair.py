######################################################
#
# Author: Davide Colombo
# Date: 11/12/21 17:32
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.env.sensor.fact as factabc
import airquality.env.env as envtype
import airquality.api.api_repo as apirepo
import airquality.api.url.purpleair as urltype
import airquality.file.parser.json_parser as parser
import airquality.api.resp.purpleair as builder
import airquality.filter.namefilt as nameflt
import airquality.filter.geolocation as geoflt
import airquality.database.exe.info as infoexe
import airquality.database.exe.geolocation as geoexe
import airquality.database.repo.info as inforepo
import airquality.database.repo.geolocation as georepo
import airquality.command.sensor as cmdtype


# ------------------------------- PurpleairEnvFact ------------------------------- #
class PurpleairEnvFact(factabc.APIEnvFactABC):

    def __init__(self, path_to_env: str, command: str, target: str):
        super(PurpleairEnvFact, self).__init__(path_to_env=path_to_env, command=command, target=target)

    ################################ craft_env() ################################
    def craft_env(self) -> envtype.Environment:
        file_logger = self.file_logger
        console_logger = self.console_logger

        url_builder = urltype.PurpleairURLBuilder(url=self.url)
        api_repo = apirepo.APIRepo(url_builder=url_builder)
        resp_parser = parser.JSONParser()
        resp_builder = builder.PurpleairAPIRespBuilder()

        db_repo = self.craft_database()
        resp_filter = self.craft_response_filter(db_repo=db_repo)
        resp_filter.set_file_logger(self.file_logger)
        resp_filter.set_console_logger(self.console_logger)

        query_executor = self.craft_query_executor(db_repo=db_repo)
        command = cmdtype.SensorCommand(
            api_repo=api_repo, resp_parser=resp_parser, resp_builder=resp_builder, resp_filter=resp_filter, query_exec=query_executor
        )
        command.set_file_logger(file_logger)
        command.set_console_logger(console_logger)

        return envtype.Environment(
            file_logger=self.file_logger,
            console_logger=self.console_logger,
            error_logger=self.error_logger,
            commands=[command]
        )

    ################################ craft_database() ################################
    def craft_database(self):
        if self.command == 'init':
            return inforepo.SensorInfoRepo(db_adapter=self.db_adapter, query_builder=self.query_builder, sensor_type=self.target)
        elif self.command == 'update':
            return georepo.SensorGeoRepo(db_adapter=self.db_adapter, query_builder=self.query_builder, sensor_type=self.target)
        else:
            raise SystemExit(f"{self.__class__.__name__} in {self.craft_database.__name__}: invalid command "
                             f"'{self.command}' for PurpleAir sensors")

    ################################ craft_response_filter() ################################
    def craft_response_filter(self, db_repo):
        if self.command == 'init':
            sensor_names = db_repo.database_sensor_names
            return nameflt.NameFilter(sensor_names)
        elif self.command == 'update':
            active_locations = db_repo.database_locations
            return geoflt.GeoFilter(active_locations)
        else:
            raise SystemExit(f"{self.__class__.__name__} in {self.craft_response_filter.__name__}: invalid command "
                             f"'{self.command}' for PurpleAir sensors")

    ################################ craft_query_executor() ################################
    def craft_query_executor(self, db_repo):
        if self.command == 'init':
            return infoexe.InfoQueryExecutor(db_repo=db_repo)
        elif self.command == 'update':
            return geoexe.GeolocationQueryExecutor(db_repo=db_repo)
        else:
            raise SystemExit(f"{self.__class__.__name__} in {self.craft_query_executor.__name__}: invalid command "
                             f"'{self.command}' for PurpleAir sensors")
