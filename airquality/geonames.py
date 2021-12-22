######################################################
#
# Author: Davide Colombo
# Date: 22/12/21 08:44
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from itertools import count
from contextlib import suppress
from airquality.sqldict import FrozenSQLDict
from airquality.mixindict import GeonamesDict
from airquality.filedict import FrozenFileDict


def geonames(geonames_dict: GeonamesDict, geoarea_dict: FrozenSQLDict, poscodes_files: FrozenFileDict):

    database_poscodes = {record[0] for record in geoarea_dict.values()}
    print(f"How much UNIQUE postal codes do we have into the database? #{len(database_poscodes)}")

    for filename in geonames_dict:
        lines = geonames_dict[filename]
        new_poscodes = {line.poscode for line in lines}
        print(f"How much UNIQUE postal codes do we have? #{len(new_poscodes)}")

        lines = poscodes_files[filename]
        new_poscodes &= {line.poscode for line in lines}
        print(f"How much UNIQUE new (not in database) PATIENT postal codes do we have? #{len(new_poscodes)}")

        new_poscodes |= database_poscodes
        new_poscodes -= database_poscodes
        print(f"How much UNIQUE new (not in database) postal codes do we have? #{len(new_poscodes)}")

        poscode_counter = count(geonames_dict.start_id)
        values = ','.join(f"({next(poscode_counter)}, {line.sql_record})" for line in geonames_dict[filename] if line.poscode in new_poscodes)
        with suppress(ValueError):
            geonames_dict.commit(values)
