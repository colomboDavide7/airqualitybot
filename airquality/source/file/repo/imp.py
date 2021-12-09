######################################################
#
# Author: Davide Colombo
# Date: 07/12/21 20:15
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from os import listdir
from os.path import isfile, join
from typing import Tuple
import airquality.source.file.repo.abc as repoabc


# ------------------------------- FileRepo ------------------------------- #
class FileRepo(repoabc.FileRepoABC):

    def __init__(self, path2directory: str):
        self.path2directory = path2directory

    ################################ get_files() ################################
    def get_files(self) -> Tuple[str]:
        return tuple([f for f in listdir(self.path2directory) if isfile(join(self.path2directory, f)) and not f.startswith('.')])
