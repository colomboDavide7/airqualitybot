######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 16:18
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import airquality.command.initsrv.cmd as cmd
import airquality.command.basefact as fact
import airquality.logger.util.decorator as log_decorator
import airquality.file.util.line_parser as parser
import airquality.file.line.builder as linebuilder
import airquality.filter.geonames as flt
import airquality.database.conn.adapt as db
import airquality.database.repo.geonames as dbrepo
import airquality.database.util.query as qry
import airquality.file.structured.json as file
import airquality.file.repo.geonames as filerepo
import airquality.source.file as filesource


class InitServiceCommandFactory(fact.CommandFactory):

    def __init__(
            self, query_file: file.JSONFile, conn: db.DatabaseAdapter,
            log_filename="log", only_new_places=True, only_patient_poscodes=True, unique_lines=True
    ):
        super(InitServiceCommandFactory, self).__init__(query_file=query_file, conn=conn, log_filename=log_filename)
        self.only_new_places = only_new_places
        self.only_patient_poscodes = only_patient_poscodes
        self.unique_lines = unique_lines

    @log_decorator.log_decorator()
    def create_command(self, sensor_type: str):
        commands_to_execute = []
        tsv_parser = parser.get_line_parser("\t", log_filename=self.log_filename)

        path2filter = f"{os.environ['directory_of_resources']}/{sensor_type}/filter"
        poscode_repo = filerepo.GeonamesFileRepo(path2filter)
        poscode_builder = linebuilder.PostalcodeLineBuilder()
        poscode_source = filesource.PostalcodeFileSource(repo=poscode_repo, parser=tsv_parser, builder=poscode_builder)

        path2geonames = f"{os.environ['directory_of_resources']}/{sensor_type}"
        geonames_repo = filerepo.GeonamesFileRepo(path2geonames)
        geonames_builder = linebuilder.GeonamesLineBuilder(log_filename=self.log_filename)
        geonames_source = filesource.GeonamesFileSource(repo=geonames_repo, parser=tsv_parser, builder=geonames_builder)

        db_repo = self.get_database_side_objects(sensor_type)

        files = geonames_source.get()
        for f in files:
            file_filter = flt.GeonamesFilter(log_filename=self.log_filename)
            if self.only_new_places:
                places = db_repo.with_country_code(f.country_code).lookup_place_names()
                file_filter.with_database_place_names(places)
            if self.only_patient_poscodes:
                poscode_file = poscode_source.retrieve(f.filename)
                file_filter.with_postalcodes(poscode_file.postal_codes)

            file_filter.set_file_logger(self.file_logger)
            file_filter.set_console_logger(self.console_logger)

            file_lines = f.lines
            if self.unique_lines:
                file_lines = f.unique_lines()

            command = cmd.ServiceInitCommand(
                file_lines=file_lines, db_repo=db_repo, file_filter=file_filter, log_filename=self.log_filename)
            command.set_console_logger(self.console_logger)
            command.set_file_logger(self.file_logger)
            commands_to_execute.append(command)
        return commands_to_execute

    def get_api_side_objects(self):
        pass

    def get_database_side_objects(self, sensor_type: str):
        query_builder = qry.QueryBuilder(self.query_file)
        return dbrepo.GeonamesRepo(db_adapter=self.database_conn, query_builder=query_builder)
