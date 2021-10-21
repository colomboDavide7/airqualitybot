#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 10:29
# @Description: this script defines a class for dynamically build valid sql queries.
#
#################################################
import builtins
from typing import List
from airquality.io.io import IOManager
from airquality.parser.file_parser import FileParserFactory


class SQLQueryBuilder(builtins.object):
    """Class that builds dynamically the sql query to be sent to the database.

    The __init__() method takes the path to the query file."""


    def __init__(self, query_file_path: str):
        self.__path = query_file_path
        self.__raw = IOManager.open_read_close_file(self.__path)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = query_file_path.split('.')[-1])
        self.__parsed = parser.parse(self.__raw)


    def select_mobile_sensor_ids(self, models: List[str]) -> str:
        """This method returns a string that contains as many queries as the models passed in the list.

        If 'models' list is empty, SystemExit exception is raised.

        If 'query_id' does not match one of the sql query identifier in 'properties/sql_query.json' file,
        SystemExit exception is raised."""

        query_id = "sensor_ids_from_model"

        if not models:
            raise SystemExit(f"{SQLQueryBuilder.__name__}: empty 'mobile' model list in method "
                             f"'{SQLQueryBuilder.select_mobile_sensor_ids.__name__}()'. "
                             f"Please check your 'properties/resources.json' file.")

        if query_id not in self.__parsed.keys():
            raise SystemExit(f"{SQLQueryBuilder.__name__}: query id '{query_id}' not found in method "
                             f"'{SQLQueryBuilder.select_mobile_sensor_ids.__name__}()'. "
                             f"Please check your 'properties/sql_query.json' file.")

        query = ""
        for model in models:
            query += self.__parsed[query_id].format(model=model)

        return query
