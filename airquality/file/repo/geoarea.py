######################################################
#
# Author: Davide Colombo
# Date: 07/12/21 20:15
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
from typing import Generator
import airquality.file.repo.repo as baserepo
import airquality.file.util.reader as read


class GeoAreaRepo(baserepo.FileRepoABC):

    def __init__(self, path2directory: str):
        super(GeoAreaRepo, self).__init__(path2directory=path2directory)

    def get_files(self) -> Generator[str, None, None]:
        for f in os.listdir(self.path2directory):
            if os.path.isfile(os.path.join(self.path2directory, f)) and not f.startswith('.'):
                yield f

    def get_file_lines(self, filename: str) -> Generator[str, None, None]:
        return read.open_readlines_close_file(os.path.join(self.path2directory, filename))

    def get_countrycode_from_filename(self, filename) -> str:
        return filename.split('.')[0]
