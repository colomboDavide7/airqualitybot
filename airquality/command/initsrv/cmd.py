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
import airquality.database.op.sel.geoarea as geosel
import airquality.database.op.ins.geoarea as geoins


class ServiceInitCommand(cmd.Command):

    def __init__(
            self,
            p2g: str,
            lp: parser.LineParser,
            lb: gl.GeonamesLineBuilder,
            lf: flt.LineFilter,
            gsw: geosel.GeographicSelectWrapper,
            giw: geoins.GeographicalAreaInsertWrapper,
            log_filename="geonames"
    ):
        super(ServiceInitCommand, self).__init__(log_filename=log_filename)
        self.line_parser = lp
        self.path2geonames = p2g
        self.line_builder = lb
        self.line_filter = lf
        self.select_wrapper = gsw
        self.insert_wrapper = giw

    @log_decorator.log_decorator()
    def execute(self):

        country_files = [f for f in os.listdir(path=self.path2geonames) if
                         os.path.isfile(os.path.join(self.path2geonames, f))]

        for f in country_files:
            lines = rdr.open_readlines_close_file(path=f"{self.path2geonames}/{f}")
            parsed_lines = self.line_parser.parse_lines(lines)
            geolines = self.line_builder.build_lines(parsed_lines)

            if not geolines:
                self.log_warning(f"{ServiceInitCommand.__name__}: empty country file => skip to next one")
                continue

            country_code = f.split('.')[0]
            self.select_wrapper.with_country_code(country_code)
            database_place_names = self.select_wrapper.select()

            filtered_lines = (geoline for geoline in uniques(geolines) if geoline.place_name not in database_place_names)

            self.insert_wrapper.insert(filtered_lines)


def uniques(geolines):
    places_with_more_than_one_occurrence = set()
    for geoline in geolines:
        if geoline.place_name not in places_with_more_than_one_occurrence:
            yield geoline
            places_with_more_than_one_occurrence.add(geoline.place_name)
