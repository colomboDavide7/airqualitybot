######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 05/11/21 17:44
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
from airquality.container.sql_container import SQLContainer, APIParamSQLContainer


class APIParamSQLContainerComposition(SQLContainer):
    """SQL container class that is a composition of APIParamSQLContainer object."""

    def __init__(self, children: List[APIParamSQLContainer]):
        self.children = children

    def sql(self) -> str:
        return ','.join(c.sql() for c in self.children)
