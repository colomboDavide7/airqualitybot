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
import airquality.database.exe.geoarea as exetype
import airquality.database.repo.geoarea as dbtype
import airquality.command.service as cmdtype


# ------------------------------- GeonamesEnvFact ------------------------------- #
class GeonamesEnvFact(factabc.EnvFactABC):

    def __init__(self, path_to_env: str, command: str, target: str):
        super(GeonamesEnvFact, self).__init__(path_to_env=path_to_env, command=command, target=target)

    ################################ craft_env() ################################
    def craft_env(self) -> envtype.Environment:
        file_logger = self.file_logger
        console_logger = self.console_logger

        path_to_src_repo = f"{self.prop_dir}/{self.target}"
        src_repo = filerepo.FileRepo(path2directory=path_to_src_repo)
        src_repo.set_file_logger(file_logger)
        src_repo.set_console_logger(console_logger)

        file_parser = parser.TSVLineParser()
        file_parser.set_file_logger(file_logger)
        file_parser.set_console_logger(console_logger)

        line_builder = builder.GeoareaLineBuilder()

        commands = []
        for f in src_repo.files:
            country_code = f.split('.')[0]
            db_repo = dbtype.GeoareaRepo(db_adapter=self.db_adapter, sql_queries=self.sql_queries, country_code=country_code)
            file_filter = self.craft_file_filter(filename=f)
            query_exec = exetype.GeoareaQueryExecutor(db_repo=db_repo)
            command = cmdtype.ServiceCommand(
                filename=f, file_repo=src_repo, file_parser=file_parser, line_builder=line_builder, file_filter=file_filter, query_exec=query_exec
            )
            commands.append(command)

        return envtype.Environment(
            file_logger=file_logger,
            console_logger=console_logger,
            error_logger=self.error_logger,
            commands=commands
        )

    ################################ craft_file_filter() ################################
    def craft_file_filter(self, filename: str) -> filtertype.GeoareaFilter:
        postalcodes = self.get_postalcodes(filename)
        places = self.get_database_places(filename)
        return filtertype.GeoareaFilter(postalcodes=postalcodes, places=places)

    ################################ get_database_places() ################################
    def get_database_places(self, filename: str, use=True) -> List[str]:
        if use:
            country_code = filename.split('.')[0]
            db_repo = dbtype.GeoareaRepo(db_adapter=self.db_adapter, sql_queries=self.sql_queries, country_code=country_code)
            return list(db_repo.places)
        return []

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
