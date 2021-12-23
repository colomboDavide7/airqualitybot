######################################################
#
# Author: Davide Colombo
# Date: 22/12/21 12:40
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
from typing import List
from airquality.dbadapter import DBAdapterABC
from airquality.filedict import FrozenFileDict
from airquality.fileline import PoscodeLine, GeonamesLine
from airquality.dbrepo import DBRepository
from airquality.sqldict import FrozenSQLDict
from airquality.mixindict import GeonamesDict


class GeonamesFactory(object):

    def __init__(self, personality: str, options: List[str], dbadapter: DBAdapterABC):
        self.personality = personality
        self.options = options
        self.dbadapter = dbadapter
        self._path_to_repo = ""
        self._included_countries = []
        self._geoarea_table = None
        self._geoarea_dict = None
        self._geonames_dict = None

    def _repo_dir(self) -> str:
        if not self._path_to_repo:
            self._path_to_repo = f"{os.environ['resource_dir']}/{os.environ['geonames_dir']}"
        return self._path_to_repo

    def _patient_poscode_dir(self) -> str:
        if self.options:
            if '-p' in self.options or '--patient_poscodes' in self.options:
                return f"{self._repo_dir()}/{os.environ['geonames_pos_dir']}"
        return ""

    def _country_data_dir(self) -> str:
        return f"{self._repo_dir()}/{os.environ['geonames_data_dir']}"

    def _country_to_include(self) -> List[str]:
        if not self._included_countries:
            self._included_countries = os.environ['geonames_included_files'].split(',')
        return self._included_countries

    @property
    def poscodes_files(self) -> FrozenFileDict:
        if self._patient_poscode_dir():
            return FrozenFileDict(path_to_dir=self._patient_poscode_dir(), include=self._country_to_include(), line_factory=PoscodeLine)
        return FrozenFileDict(path_to_dir=self._country_data_dir(), include=self._country_to_include(), line_factory=GeonamesLine)

    @property
    def geoarea_dict(self):
        if self._geoarea_dict is None:
            self._geoarea_dict = FrozenSQLDict(table=DBRepository.geoarea_table(), dbadapter=self.dbadapter)
        return self._geoarea_dict

    @property
    def service_dict(self) -> FrozenSQLDict:
        return FrozenSQLDict(table=DBRepository.filtered_service_table(requested_type=self.personality), dbadapter=self.dbadapter)

    @property
    def geonames_dict(self):
        if self._geonames_dict is None:
            self._geonames_dict = GeonamesDict(
                path_to_dir=self._country_data_dir(),
                include=self._country_to_include(),
                table=DBRepository.geoarea_table(),
                dbadapter=self.dbadapter,
                line_factory=GeonamesLine
            )
        return self._geonames_dict
