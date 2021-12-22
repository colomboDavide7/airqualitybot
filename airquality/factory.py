######################################################
#
# Author: Davide Colombo
# Date: 22/12/21 12:40
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
from typing import List


class GeonamesFactory(object):

    def __init__(self, personality: str, options: List[str]):
        self.personality = personality
        self.options = options
        self._path_to_repo = ""

    @property
    def path_to_repo(self) -> str:
        if not self._path_to_repo:
            self._path_to_repo = f"{os.environ['resource_dir']}/{os.environ[f'{self.personality}_dir']}"
        return self._path_to_repo

    @property
    def patient_poscode_dir(self) -> str:
        if self.options:
            if '-p' in self.options or '--patient_poscodes' in self.options:
                return f"{self.path_to_repo}/{os.environ[f'{self.personality}_pos_dir']}"
        return ""

    @property
    def country_data_dir(self) -> str:
        return f"{self.path_to_repo}/{os.environ[f'{self.personality}_data_dir']}"

    @property
    def country_to_include(self) -> List[str]:
        return os.environ[f'{self.personality}_included_files'].split(',')
