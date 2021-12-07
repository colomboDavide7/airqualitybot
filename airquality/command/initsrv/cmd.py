######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 16:18
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import airquality.logger.util.decorator as log_decorator
import airquality.command.basecmd as cmd
import airquality.file.util.line_parser as parser
import airquality.file.line.geobuilder as gl
import airquality.filter.linefilt as flt
import airquality.database.repo.geoarea as dbrepo
import airquality.file.repo.geoarea as filerepo


class ServiceInitCommand(cmd.Command):

    def __init__(
            self,
            path2filter: str,
            lp: parser.LineParser,
            lb: gl.GeonamesLineBuilder,
            lf: flt.LineFilter,
            file_repo: filerepo.GeoAreaRepo,
            db_repo: dbrepo.GeoAreaRepo,
            log_filename="geonames"
    ):
        super(ServiceInitCommand, self).__init__(log_filename=log_filename)
        self.line_parser = lp
        self.path2filter = path2filter
        self.line_builder = lb
        self.line_filter = lf
        self.file_repo = file_repo
        self.db_repo = db_repo

    @log_decorator.log_decorator()
    def execute(self):

        filter_files = [f for f in os.listdir(path=self.path2filter) if os.path.isfile(os.path.join(self.path2filter, f))]

        files = self.file_repo.get_files()
        for f in files:
            lines = self.file_repo.get_file_lines(f)
            parsed_lines = self.line_parser.parse_lines(lines)
            geolines = self.line_builder.build_lines(parsed_lines)

            # for ff in filter_files:
            #     if country_code in ff:
            #         lines = rdr.open_readlines_close_file(path=f"{self.path2filter}/{f}")
            #         parsed_lines = self.line_parser.parse_lines(lines)
            #         postalcode2keep = [p[0] for p in parsed_lines]
            #         self.line_filter.with_postal_code2keep(postalcode2keep)

            filtered_lines = self.line_filter.filter(geolines)

            self.db_repo.with_country_code(self.file_repo.get_countrycode_from_filename(f)).push(filtered_lines)
