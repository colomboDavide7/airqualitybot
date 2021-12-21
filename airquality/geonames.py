######################################################
#
# Author: Davide Colombo
# Date: 21/12/21 10:09
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from itertools import count
from typing import List
from airquality.dbadapter import DBAdapterABC
from airquality.filedict import FrozenFileDict
from airquality.sqltable import FilterSQLTable
from airquality.sqldict import HeavyweightMutableSQLDict


GEOGRAPHICAL_AREA_COLS = ['postal_code', 'country_code', 'place_name', 'province', 'state', 'geom']
ST_GEOM_FROM_TEXT = "ST_GeomFromText('{geom}', {srid})"
POSTGIS_POINT = "POINT({lon} {lat})"


def strip_extension(filename: str) -> str:
    return filename.split('.')[0]


def clean_value(string: str) -> str:
    return string.replace("'", "")


def geonames(path_to_repo: str, data_dir: str, include: List[str], dbadapter: DBAdapterABC, patient_poscodes_dir: str = ""):

    frozen_data_files = FrozenFileDict(path_to_dir=f"{path_to_repo}/{data_dir}", include=include)
    print(repr(frozen_data_files))

    if patient_poscodes_dir:
        frozen_poscodes_files = FrozenFileDict(path_to_dir=f"{path_to_repo}/{patient_poscodes_dir}", include=include)
        print(repr(frozen_poscodes_files))

    for f in frozen_data_files:
        print(f"looking at country '{strip_extension(f)}'")
        country_table = FilterSQLTable(table_name="geographical_area", pkey="id", selected_cols=GEOGRAPHICAL_AREA_COLS,
                                       filter_col="country_code", filter_val=strip_extension(f))
        heavyweight_mutable_dict = HeavyweightMutableSQLDict(table=country_table, dbadapter=dbadapter)

        print(repr(heavyweight_mutable_dict))
        print(len(heavyweight_mutable_dict))

        # Create a Set for speed-up the lookup with the downside of wasting more memory
        database_poscodes = {record[0] for pkey, record in heavyweight_mutable_dict.items()}

        lines = frozen_data_files[f]
        parsed_lines = (line.split('\t') for line in lines)
        new_poscodes = {line[1] for line in parsed_lines}
        print(f"How much UNIQUE postal codes do we have? #{len(new_poscodes)}")

        new_poscodes |= database_poscodes
        new_poscodes -= database_poscodes
        print(f"How much UNIQUE new postal codes do we have? #{len(new_poscodes)}")

        if patient_poscodes_dir:
            new_poscodes &= set(frozen_poscodes_files[f])
            print(f"How much UNIQUE new postal codes INTERSECTED to patient postal codes do we have? #{len(new_poscodes)}")

        poscode_counter = count(heavyweight_mutable_dict.start_id)

        lines = frozen_data_files[f]
        for line in lines:
            country, poscode, place, state, state_code, prov, prov_code, comm, comm_code, lat, lon, acc = line.split('\t')
            if poscode in new_poscodes:
                # print(f"found new place '{place}' in {country} with postal code {poscode}")
                point = POSTGIS_POINT.format(lat=lat, lon=lon)
                geom = ST_GEOM_FROM_TEXT.format(geom=point, srid=26918)
                heavyweight_mutable_dict[next(poscode_counter)] = \
                    f"'{poscode}', '{country}', '{clean_value(place)}', '{clean_value(prov)}', '{clean_value(state)}', {geom}"

        if next(poscode_counter) != heavyweight_mutable_dict.start_id:
            print(f"found new places to commit!")
            heavyweight_mutable_dict.commit()
