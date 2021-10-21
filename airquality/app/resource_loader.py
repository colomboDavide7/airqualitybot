#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 19:28
# @Description: this file defines a resource loader class
#
#################################################
import builtins
from airquality.io.io import IOManager
from airquality.app.session import Session
from airquality.parser.parser import ParserFactory
from airquality.conn.conn import DatabaseConnectionAdapterFactory
from airquality.app.db_settings_builder import DatabaseSettingsBuilder


class ResourceLoader(builtins.object):
    """
    This class is used for loading the resources during application setup.

    - path:         the path to the resource file
    - session:      the Session object for local debugging
    - content:      the raw content of the resource file
    - resources:    the parsed content of the resource file
    - conn_created: flag that tells whether the db conn has been created
    """

    def __init__(self,
                 path: str,
                 session: Session):
        self.__path = path
        self.__session = session
        self.__raw = None
        self.__parsed = None
        self.__conn_created = False


    def load_resources(self) -> bool:
        """
        This function asks the IOManager to load resources from the 'path'

        If 'content' is not None, SystemExit exception is raised.
        """
        if self.__raw is not None:
            raise SystemExit(f"{ResourceLoader.__name__}: resources are already loaded.")

        self.__raw = IOManager.open_read_close_file(path = self.__path)
        return True


    def parse_resources(self) -> bool:
        """
        This method parses the resources if content is not None,
        otherwise a SystemExit error is raised.

        A Parser object is obtained from the ParserFactory depending on the
        resource file extension.

        If the file extension is not supported, ParserFactory raises TypeError
        and this method catches it and raises SystemExit exception.

        If 'resources' are already loaded, SystemExit exception is raised.
        """
        if self.__raw is None:
            raise SystemExit(
                    f"{ResourceLoader.__name__}: "
                    f"raw content is empty. You must call method "
                    f"'{ResourceLoader.load_resources.__name__}' "
                    f"before '{ResourceLoader.parse_resources.__name__}'.")

        if self.__parsed is not None:
            raise SystemExit(f"{ResourceLoader.__name__}: "
                             f"resources already parsed.")

        try:
            parser = ParserFactory.make_parser_from_extension_file(file_extension = self.__path.split('.')[-1],
                                                                   raw_content    = self.__raw)
            self.__session.debug_msg(f"{ResourceLoader.__name__}: parser created successfully: type {parser.__class__.__name__}")
            self.__session.debug_msg(f"{ResourceLoader.__name__}: try to parse resources")
            self.__parsed = parser.parse()
            self.__session.debug_msg(f"{ResourceLoader.__name__}: resources parsed successfully")
        except TypeError as terr:
            raise SystemExit(f"{ResourceLoader.__name__}: " + str(terr))
        return True


    def database_connection(self, username: str):
        """
        This method return a new DatabaseConnection if 'conn_created'
        is False, otherwise SystemExit exception is raised.

        If resources are not parsed, a SystemExit exception is raised.

        This method asks the DatabaseSettingsBuilder to builds the correct
        settings dictionary from the parsed resources to feed them into the
        DatabaseConnection constructor.
        """
        if self.__parsed is None:
            raise SystemExit(f"{ResourceLoader.__name__}: 'resources' is empty. "
                             f"You must call '{self.parse_resources.__name__}()' "
                             f"before '{self.database_connection.__name__}()'.")

        if self.__conn_created:
            raise SystemExit(f"{ResourceLoader.__name__}: connection already created.")

        self.__conn_created = True
        dbfactory = DatabaseConnectionAdapterFactory()
        settings = DatabaseSettingsBuilder.create_db_settings_from_parsed_resources_for_user(self.__parsed, username)
        return dbfactory.create_connection(settings)


    def sensor_models(self, sensor_type: str):
        return DatabaseSettingsBuilder.list_models_from_type(self.__parsed, sensor_type)


    def __str__(self):
        return f"{ResourceLoader.__name__}: " \
               f"\'path\'={self.__path}"
