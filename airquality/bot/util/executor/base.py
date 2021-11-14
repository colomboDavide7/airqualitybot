######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 14/11/21 21:59
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List
import airquality.database.conn as db
import airquality.database.util.sql.query as query
import airquality.logger.log as log


class QueryExecutor(abc.ABC):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder):
        self.conn = conn
        self.builder = query_builder
        self.logger = None
        self.debugger = None

    def set_logger(self, logger: log.logging.Logger):
        self.logger = logger

    def set_debugger(self, debugger: log.logging.Logger):
        self.debugger = debugger

    def log_messages(self, messages: List[str]):
        for msg in messages:
            if self.logger:
                self.logger.info(msg)
            if self.debugger:
                self.debugger.info(msg)
