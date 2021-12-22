######################################################
#
# Author: Davide Colombo
# Date: 22/12/21 08:44
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
GEOGRAPHICAL_AREA_COLS = ['postal_code', 'country_code', 'place_name', 'province', 'state', 'geom']

from typing import List
from itertools import count
from airquality.dbadapter import DBAdapterABC
from airquality.filedict import FrozenFileDict
from airquality.sqltable import SQLTable
from airquality.sqldict import FrozenSQLDict
from airquality.mixindict import GeonamesDict
from contextlib import suppress


def strip_extension(filename: str) -> str:
    """Remove the extension from the *filename* argument

    >>> strip_extension("test.txt")
    test
    """

    return filename.split('.')[0]


def geonames(path_to_repo: str, data_dir: str, include: List[str], dbadapter: DBAdapterABC, patient_poscodes_dir: str = ""):

    frozen_poscodes_files = None
    if patient_poscodes_dir:
        frozen_poscodes_files = FrozenFileDict(path_to_dir=f"{path_to_repo}/{patient_poscodes_dir}", include=include)
        print(repr(frozen_poscodes_files))

    geoarea_table = SQLTable(table_name="geographical_area", pkey="id", selected_cols=GEOGRAPHICAL_AREA_COLS)
    geonames_dict = GeonamesDict(path_to_dir=f"{path_to_repo}/{data_dir}", include=include, table=geoarea_table, dbadapter=dbadapter)

    # Create a local (to the function) FrozenSQLDict on 'geographical_area' to get the database postcodes
    geoarea_frozen_dict = FrozenSQLDict(table=geoarea_table, dbadapter=dbadapter)
    database_poscodes = {record[0] for record in geoarea_frozen_dict.values()}
    print(f"How much UNIQUE postal codes do we have into the database? #{len(database_poscodes)}")

    for filename in geonames_dict:
        print(f"looking at country '{strip_extension(filename)}'")

        lines = geonames_dict[filename]
        new_poscodes = {line.poscode for line in lines}
        print(f"How much UNIQUE postal codes do we have? #{len(new_poscodes)}")

        new_poscodes |= database_poscodes
        new_poscodes -= database_poscodes
        print(f"How much UNIQUE new (not in database) postal codes do we have? #{len(new_poscodes)}")

        if frozen_poscodes_files is not None:
            new_poscodes &= set(frozen_poscodes_files[filename])
            print(f"How much UNIQUE new (not in database) PATIENT postal codes do we have? #{len(new_poscodes)}")

        poscode_counter = count(geonames_dict.start_id)
        values = ','.join(f"({next(poscode_counter)}, {line.sql_record})" for line in geonames_dict[filename] if line.poscode in new_poscodes)
        with suppress(ValueError):
            geonames_dict.commit(values)
