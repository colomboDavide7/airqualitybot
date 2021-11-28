######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 15:24
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.database.conn.adapt as conn

ACTIVE_ADAPTERS: List[conn.DatabaseAdapter] = []


def shutdown():
    for adapter in ACTIVE_ADAPTERS:
        adapter.close_conn()
    ACTIVE_ADAPTERS.clear()
