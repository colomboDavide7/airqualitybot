######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 15:31
# Description: this script defines a set of classes that encapsulate the logic of transforming an API packet into
#              a valid query.
#
######################################################
import builtins
from typing import List
from airquality.packet.packet import Packet
from airquality.constants.shared_constants import EMPTY_LIST


class BridgeObject(builtins.object):

    def __init__(self, packets: List[Packet]):
        self.packets = packets

    def packets2query(self) -> str:

        if self.packets == EMPTY_LIST:
            return ""

        sqlquery = ""
        for packet in self.packets:
            sqlquery += packet.sql() + ","

        sqlquery = sqlquery.strip(',') + ';'
        return sqlquery
