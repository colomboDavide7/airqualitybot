######################################################
#
# Author: Davide Colombo
# Date: 21/12/21 10:09
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
from airquality.frozenfiledict import FrozenFileDict


def geonames(path_to_repo: str, data_dir: str, include: List[str], patient_poscodes_dir: str = ""):

    data_files = FrozenFileDict(path_to_dir=f"{path_to_repo}/{data_dir}", include=include)
    print(repr(data_files))

    print(data_files["bad_filename.txt"])

    if patient_poscodes_dir:
        poscodes_files = FrozenFileDict(path_to_dir=f"{path_to_repo}/{patient_poscodes_dir}", include=include)
        print(repr(poscodes_files))
