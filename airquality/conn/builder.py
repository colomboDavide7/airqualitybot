#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 10:29
# @Description: This script contains a class that defines methods for getting
#               queries
#
#################################################
import builtins
from typing import List
from airquality.io.io import IOManager
from airquality.parser.parser import ParserFactory


class SQLQueryBuilder(builtins.object):
    """
    Class that builds dynamically the sql query to be sent through the database
    connection adapter to the database.

    The __init__() method take the 'query_file_path' argument that defines where
    it is located the query file.

    During initialization, it is asked the IOManager to read the content of the file.
    Then the ParserFactory returns the proper Parser object.
    The parser is used to parse the file.
    Parsed content is stored in an instance variable, so is available at any time
    to this instance.
    """

    def __init__(self, query_file_path: str):
        self.__path = query_file_path
        self.__raw = IOManager.open_read_close_file(self.__path)

        parser = ParserFactory.make_parser_from_extension_file(
                file_extension = query_file_path.split('.')[-1],
                raw_content = self.__raw
        )

        self.__parsed = parser.parse()


    def select_mobile_sensor_ids(self, models: List[str]) -> str:
        """
        This method returns a string object that contains as many queries as the
        models passed in the list. Each query can be executed for selecting the
        sensor ids from the database.

        The query_id is used to identify which field to use for retrieving the sql
        query from the parsed data for building the query."""

        query_id = "mobile_sensor_ids"

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
