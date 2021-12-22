######################################################
#
# Author: Davide Colombo
# Date: 22/12/21 10:25
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Generator
from airquality.fileline import GeonamesLine
from airquality.sqltable import SQLTableABC
from airquality.dbadapter import DBAdapterABC
from airquality.filedict import FrozenFileDict


class GeonamesDict(FrozenFileDict):

    def __init__(self, path_to_dir: str, include: List[str], table: SQLTableABC, dbadapter: DBAdapterABC, line_factory=GeonamesLine):
        super(GeonamesDict, self).__init__(path_to_dir=path_to_dir, include=include, line_factory=line_factory)
        self.table = table
        self.dbadapter = dbadapter

    @property
    def start_id(self) -> int:
        row = self.dbadapter.fetch_one(f"SELECT MAX({self.table.pkey}) FROM {self.table.schema}.{self.table.name};")
        return 1 if row[0] is None else row[0] + 1

    def commit(self, values: str):
        if not values:
            raise ValueError(f"{type(self).__name__} in commit(): cannot commit empty values to {self.table!r}")
        self.dbadapter.execute(f"INSERT INTO {self.table.schema}.{self.table.name} VALUES {values};")

    def __getitem__(self, filename) -> Generator[GeonamesLine, None, None]:
        return super(GeonamesDict, self).__getitem__(filename)

    def __repr__(self):
        return super(GeonamesDict, self).__repr__().strip(')') + f", table={self.table!r}, dbadapter={self.dbadapter!r})"
