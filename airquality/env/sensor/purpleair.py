######################################################
#
# Author: Davide Colombo
# Date: 11/12/21 17:32
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict
import airquality.env.sensor.fact as factabc
import airquality.env.env as envtype
import airquality.api.deprecated_repo as apirepo
import api.urlfmt as urltype
import airquality.file.parser.json_parser as parser
import airquality.api.resp.purpleair as builder
import airquality.filter.nameflt as nameflt
import airquality.filter.geoflt as geoflt
import airquality.command.sensor as cmdtype
import airquality.database.repo.info as sqlinfo
import airquality.database.repo.geolocation as sqlgeo


# ------------------------------- PurpleairEnvFact ------------------------------- #
class PurpleairEnvFact(factabc.APIEnvFactABC):

    def __init__(self, path_to_env: str, command: str, target: str):
        super(PurpleairEnvFact, self).__init__(path_to_env=path_to_env, command=command, target=target)
        self._id2name = None

    @property
    def database_sensor_names(self) -> List[str]:
        query2exec = self.sql_queries.s4.format(target=self.target)
        db_lookup = self.db_conn.execute(query2exec)
        return [item[0] for item in db_lookup]

    @property
    def max_sensor_id(self) -> int:
        query2exec = self.sql_queries.s1
        db_lookup = self.db_conn.execute(query2exec)
        max_id = db_lookup[0][0]
        return 1 if max_id is None else (max_id + 1)

    @property
    def sensor_name2id(self) -> Dict[str, int]:
        query2exec = self.sql_queries.s3.format(target=self.target)
        db_lookup = self.db_conn.execute(query2exec)
        return {sensor_name: sensor_id for sensor_id, sensor_name in db_lookup}

    @property
    def sensor_id2name(self) -> Dict[int, str]:
        if self._id2name is None:
            query2exec = self.sql_queries.s3.format(target=self.target)
            db_lookup = self.db_conn.execute(query2exec)
            return {sensor_id: sensor_name for sensor_id, sensor_name in db_lookup}
        return self._id2name

    @property
    def name2geom_as_text(self) -> Dict[str, str]:
        sensor_ids_string = ','.join(f"{sensor_id}" for sensor_id in self.sensor_id2name)
        query2exec = self.sql_queries.s6.format(ids=sensor_ids_string)
        geo_lookup = self.db_conn.execute(query2exec)
        return {self.sensor_id2name[sensor_id]: geom for sensor_id, geom in geo_lookup}

    ################################ craft_env() ################################
    def craft_env(self) -> envtype.Environment:
        url_builder = urltype.DefaultURLFormatter(url_template=self.url)
        api_repo = apirepo.APIRepo(url_builder=url_builder)
        resp_parser = parser.JSONParser()
        resp_builder = builder.PurpleairAPIRespBuilder()

        resp_filter = self.craft_response_filter()
        resp_filter.set_file_logger(self.file_logger)
        resp_filter.set_console_logger(self.console_logger)

        db_repo = self.craft_database_repo()
        command = cmdtype.SensorCommand(
            api_repo=api_repo, resp_parser=resp_parser, resp_builder=resp_builder, resp_filter=resp_filter, db_repo=db_repo
        )
        command.set_file_logger(self.file_logger)
        command.set_console_logger(self.console_logger)

        return envtype.Environment(
            file_logger=self.file_logger,
            console_logger=self.console_logger,
            error_logger=self.error_logger,
            commands=[command]
        )

    ################################ craft_database_repo() ################################
    def craft_database_repo(self):
        if self.command == 'init':
            return sqlinfo.InfoDBRepo(start_id=self.max_sensor_id, db_adapter=self.db_conn, sql_queries=self.sql_queries)
        elif self.command == 'update':
            return sqlgeo.GeolocationDBRepo(sensor_name2id=self.sensor_name2id, db_adapter=self.db_conn, sql_queries=self.sql_queries)
        else:
            raise SystemExit(f"{self.__class__.__name__} in {self.craft_database_repo.__name__}: invalid command "
                             f"'{self.command}' for PurpleAir sensors")

    ################################ craft_response_filter() ################################
    def craft_response_filter(self):
        if self.command == 'init':
            return nameflt.NameFilter(names=self.database_sensor_names)
        elif self.command == 'update':
            return geoflt.GeolocationFilter(name2geom_as_text=self.name2geom_as_text)
        else:
            raise SystemExit(f"{self.__class__.__name__} in {self.craft_response_filter.__name__}: invalid command "
                             f"'{self.command}' for PurpleAir sensors")
