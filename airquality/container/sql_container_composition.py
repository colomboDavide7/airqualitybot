######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 05/11/21 17:44
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
from airquality.container.sql_container import SQLContainer


# class SQLContainerComposition(SQLContainer):
#
#     def __init__(self, containers: List[SQLContainer]):
#         self.containers = containers
#
#     def sql(self, query: str) -> str:
#         for c in self.containers:
#             query += c.sql(query="") + ','
#         return query.strip(',') + ';'

