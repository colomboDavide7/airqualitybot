######################################################
#
# Author: Davide Colombo
# Date: 08/12/21 14:31
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Tuple
import airquality.source.source as basesource
import airquality.file.repo.geonames as filerepo
import airquality.file.util.reader as filereader
import airquality.file.util.line_parser as lineparser
import airquality.file.line.builder as linebuilder
import airquality.types.file.type as filetype


def get_filename(file: str) -> str:
    return file.split('.')[0]


class FileSourceABC(basesource.SourceABC, abc.ABC):

    @abc.abstractmethod
    def get(self) -> Tuple[filetype.FileTypeABC]:
        pass

    @abc.abstractmethod
    def retrieve(self, filename: str) -> filetype.FileTypeABC:
        pass


class GeonamesFileSource(FileSourceABC):

    def __init__(self, repo: filerepo.GeonamesFileRepo, parser: lineparser.LineParser, builder: linebuilder.GeonamesLineBuilder):
        self.repo = repo
        self.parser = parser
        self.builder = builder

    def get(self) -> Tuple[filetype.GeonamesFileType]:
        files = []
        for f in self.repo.get_files():
            raw_lines = filereader.open_readlines_close_file(path=f"{self.repo.path2directory}/{f}")
            parsed_lines = self.parser.parse_lines(raw_lines)
            geolines = self.builder.build_lines(parsed_lines)
            files.append(filetype.GeonamesFileType(filename=get_filename(f), geolines=geolines))
        return tuple(files)

    def retrieve(self, filename: str) -> filetype.GeonamesFileType:
        for f in self.repo.get_files():
            fname = get_filename(f)
            if fname == filename:
                raw_lines = filereader.open_readlines_close_file(path=f"{self.repo.path2directory}/{f}")
                parsed_lines = self.parser.parse_lines(raw_lines)
                geolines = self.builder.build_lines(parsed_lines)
                return filetype.GeonamesFileType(filename=fname, geolines=geolines)


class PostalcodeFileSource(FileSourceABC):

    def __init__(self, repo: filerepo.GeonamesFileRepo, parser: lineparser.LineParser, builder: linebuilder.PostalcodeLineBuilder):
        self.repo = repo
        self.parser = parser
        self.builder = builder

    def get(self) -> Tuple[filetype.PostalcodeFileType]:
        files = []
        for f in self.repo.get_files():
            raw_lines = filereader.open_readlines_close_file(path=f"{self.repo.path2directory}/{f}")
            parsed_lines = self.parser.parse_lines(raw_lines)
            poscode_lines = self.builder.build_lines(parsed_lines)
            files.append(filetype.PostalcodeFileType(filename=get_filename(f), poscode_lines=poscode_lines))
        return tuple(files)

    def retrieve(self, filename: str) -> filetype.PostalcodeFileType:
        for f in self.repo.get_files():
            fname = get_filename(f)
            if fname == filename:
                raw_lines = filereader.open_readlines_close_file(path=f"{self.repo.path2directory}/{f}")
                parsed_lines = self.parser.parse_lines(raw_lines)
                poscode_lines = self.builder.build_lines(parsed_lines)
                return filetype.PostalcodeFileType(filename=fname, poscode_lines=poscode_lines)
