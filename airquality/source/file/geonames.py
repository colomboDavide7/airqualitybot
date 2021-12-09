######################################################
#
# Author: Davide Colombo
# Date: 08/12/21 14:31
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Tuple, Generator
import airquality.source.file.repo.imp as filerepo
import airquality.source.file.abc as filesrcabc
import airquality.file.util.reader as filereader
import airquality.file.util.line_parser as lineparser
import airquality.source.file.line.geonames as linetype


# ------------------------------- GeonamesFileType ------------------------------- #
class GeonamesFileType(filesrcabc.FileTypeABC):

    def __init__(self, filename: str, geolines: Generator[linetype.GeonamesLineType, None, None]):
        super(GeonamesFileType, self).__init__(filename=filename, lines=geolines)
        self.lines = geolines

    ################################ unique_lines() ################################
    def unique_lines(self) -> Generator[linetype.GeonamesLineType, None, None]:
        place_with_more_than_one_occurrence = set()
        for line in self.lines:
            if line.place_name not in place_with_more_than_one_occurrence:
                yield line
                place_with_more_than_one_occurrence.add(line.place_name)


# ------------------------------- GeonamesFileSource ------------------------------- #
class GeonamesFileSource(filesrcabc.FileSourceABC):

    def __init__(self, repo: filerepo.FileRepo, parser: lineparser.LineParser, builder: linetype.GeonamesLineBuilder):
        self.repo = repo
        self.parser = parser
        self.builder = builder

    ################################ get() ################################
    def get(self) -> Tuple[GeonamesFileType]:
        files = []
        for f in self.repo.get_files():
            raw_lines = filereader.open_readlines_close_file(path=f"{self.repo.path2directory}/{f}")
            parsed_lines = self.parser.parse_lines(raw_lines)
            geolines = self.builder.build_lines(parsed_lines)
            files.append(GeonamesFileType(filename=filesrcabc.get_filename(f), geolines=geolines))
        return tuple(files)

    ################################ retrieve() ################################
    def retrieve(self, filename: str) -> GeonamesFileType:
        for f in self.repo.get_files():
            fname = filesrcabc.get_filename(f)
            if fname == filename:
                raw_lines = filereader.open_readlines_close_file(path=f"{self.repo.path2directory}/{f}")
                parsed_lines = self.parser.parse_lines(raw_lines)
                geolines = self.builder.build_lines(parsed_lines)
                return GeonamesFileType(filename=fname, geolines=geolines)
