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
import airquality.file.util.reader as rdr
import airquality.file.line.geobuilder as gl
import airquality.filter.linefilt as flt
import airquality.database.repo.geoarea as dbrepo


class ServiceInitCommand(cmd.Command):

    def __init__(
            self,
            p2g: str,
            path2filter: str,
            lp: parser.LineParser,
            lb: gl.GeonamesLineBuilder,
            lf: flt.LineFilter,
            repo: dbrepo.GeoAreaRepo,
            log_filename="geonames"
    ):
        super(ServiceInitCommand, self).__init__(log_filename=log_filename)
        self.line_parser = lp
        self.path2geonames = p2g
        self.path2filter = path2filter
        self.line_builder = lb
        self.line_filter = lf
        self.repo = repo

    @log_decorator.log_decorator()
    def execute(self):

        country_files = [f for f in os.listdir(path=self.path2geonames) if os.path.isfile(os.path.join(self.path2geonames, f))
                         and not f.startswith('.')]
        filter_files = [f for f in os.listdir(path=self.path2filter) if os.path.isfile(os.path.join(self.path2filter, f))]

        for f in country_files:
            lines = rdr.open_readlines_close_file(path=f"{self.path2geonames}/{f}")
            parsed_lines = self.line_parser.parse_lines(lines)
            geolines = self.line_builder.build_lines(parsed_lines)

            country_code = f.split('.')[0]

            # for ff in filter_files:
            #     if country_code in ff:
            #         lines = rdr.open_readlines_close_file(path=f"{self.path2filter}/{f}")
            #         parsed_lines = self.line_parser.parse_lines(lines)
            #         postalcode2keep = [p[0] for p in parsed_lines]
            #         self.line_filter.with_postal_code2keep(postalcode2keep)

            filtered_lines = self.line_filter.filter(geolines)

            self.repo.with_country_code(country_code).push(filtered_lines)
