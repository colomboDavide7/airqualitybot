######################################################
#
# Author: Davide Colombo
# Date: 09/12/21 17:30
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Tuple, Generator
import airquality.source.file.repo.imp as filerepo
import airquality.source.file.abc as filesrcabc
import airquality.file.util.reader as filereader
import airquality.file.util.line_parser as lineparser
import airquality.source.file.line.postalcode as linetype


# ------------------------------- PostalcodeFileType ------------------------------- #
class PostalcodeFileType(filesrcabc.FileTypeABC):

    def __init__(self, filename: str, poscode_lines: Generator[linetype.PostalcodeLineType, None, None]):
        super(PostalcodeFileType, self).__init__(filename=filename, lines=poscode_lines)
        self.lines = poscode_lines

    ################################ unique_lines() ################################
    def unique_lines(self) -> Generator[linetype.PostalcodeLineType, None, None]:
        poscode_with_more_than_one_occurrence = set()
        for line in self.lines:
            if line.postal_code not in poscode_with_more_than_one_occurrence:
                yield line
                poscode_with_more_than_one_occurrence.add(line.postal_code)


# ------------------------------- PostalcodeFileSource ------------------------------- #
class PostalcodeFileSource(filesrcabc.FileSourceABC):

    def __init__(self, repo: filerepo.FileRepo, parser: lineparser.LineParser, builder: linetype.PostalcodeLineBuilder):
        self.repo = repo
        self.parser = parser
        self.builder = builder

    ################################ get() ################################
    def get(self) -> Tuple[PostalcodeFileType]:
        files = []
        for f in self.repo.get_files():
            raw_lines = filereader.open_readlines_close_file(path=f"{self.repo.path2directory}/{f}")
            parsed_lines = self.parser.parse_lines(raw_lines)
            poscode_lines = self.builder.build_lines(parsed_lines)
            files.append(PostalcodeFileType(filename=filesrcabc.get_filename(f), poscode_lines=poscode_lines))
        return tuple(files)

    ################################ retrieve() ################################
    def retrieve(self, filename: str) -> PostalcodeFileType:
        for f in self.repo.get_files():
            fname = filesrcabc.get_filename(f)
            if fname == filename:
                raw_lines = filereader.open_readlines_close_file(path=f"{self.repo.path2directory}/{f}")
                parsed_lines = self.parser.parse_lines(raw_lines)
                poscode_lines = self.builder.build_lines(parsed_lines)
                return PostalcodeFileType(filename=fname, poscode_lines=poscode_lines)
