######################################################
#
# Author: Davide Colombo
# Date: 10/12/21 17:49
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.env.fact as factabc
import airquality.env.env as envtype
import airquality.file.repo.imp as filerepo
import airquality.file.parser.line_parser as parser
import airquality.file.line.geonames as builder
import airquality.file.line.postalcode as posbuilder
import airquality.filter.geoarea as filtertype
import airquality.database.sql.geoarea as sqltype
import airquality.command.service as cmdtype


# ------------------------------- GeonamesEnvFact ------------------------------- #
class GeonamesEnvFact(factabc.EnvFactABC):

    def __init__(self, path_to_env: str, command: str, target: str):
        super(GeonamesEnvFact, self).__init__(path_to_env=path_to_env, command=command, target=target)

    ################################ craft_env() ################################
    def craft_env(self) -> envtype.Environment:
        path_to_src_repo = f"{self.prop_dir}/{self.target}"
        src_repo = filerepo.FileRepo(path2directory=path_to_src_repo)
        src_repo.set_file_logger(self.file_logger)
        src_repo.set_console_logger(self.console_logger)

        file_parser = parser.TSVLineParser()
        file_parser.set_file_logger(self.file_logger)
        file_parser.set_console_logger(self.console_logger)

        line_builder = builder.GeoareaLineBuilder()
        db_repo = sqltype.GeoareaDBRepo(db_adapter=self.db_adapter, sql_queries=self.sql_queries)

        commands = []
        for f in src_repo.files:
            database_places = self.get_database_places(filename=f)
            file_filter = self.craft_file_filter(filename=f, database_places=database_places)
            command = cmdtype.ServiceCommand(
                filename=f, file_repo=src_repo, file_parser=file_parser, line_builder=line_builder, file_filter=file_filter, db_repo=db_repo
            )
            commands.append(command)

        return envtype.Environment(
            file_logger=self.file_logger,
            console_logger=self.console_logger,
            error_logger=self.error_logger,
            commands=commands
        )

    ################################ craft_file_filter() ################################
    def craft_file_filter(self, filename: str, database_places: List[str]) -> filtertype.GeoareaFilter:
        postalcodes = self.get_postalcodes(filename)
        return filtertype.GeoareaFilter(postalcodes=postalcodes, places=database_places)

    ################################ get_database_places() ################################
    def get_database_places(self, filename: str) -> List[str]:
        country_code = filename.split('.')[0]
        query2exec = self.sql_queries.s13.format(cc=country_code)
        db_lookup = self.db_adapter.execute(query2exec)
        return [item[0] for item in db_lookup]

    ################################ get_postalcodes() ################################
    def get_postalcodes(self, filename: str, keep=False) -> List[str]:
        if keep:
            path_to_filter_repo = f"{self.prop_dir}/{self.target}/filter"
            file_parser = parser.TSVLineParser()
            file_parser.set_file_logger(self.file_logger)
            file_parser.set_console_logger(self.console_logger)

            filter_repo = filerepo.FileRepo(path2directory=path_to_filter_repo)
            filter_repo.set_file_logger(self.file_logger)
            filter_repo.set_console_logger(self.console_logger)

            pos_line_builder = posbuilder.PostalcodeLineBuilder()

            file_content = filter_repo.read_file(filename)
            parsed_content = file_parser.parse(file_content)
            poscodes = pos_line_builder.build(parsed_content)
            return [pos.postal_code for pos in poscodes]
        return []
