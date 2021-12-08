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


class GeonamesFileRepo(baserepo.FileRepoABC):

    def __init__(self, path2directory: str):
        super(GeonamesFileRepo, self).__init__(path2directory=path2directory)

    def get_files(self) -> Generator[str, None, None]:
        for f in os.listdir(self.path2directory):
            if os.path.isfile(os.path.join(self.path2directory, f)) and not f.startswith('.'):
                yield f
