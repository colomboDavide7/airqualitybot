#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 19:28
# @Description: this file defines a resource loader class
#
#################################################
import builtins

from airquality.app.session import Session
from airquality.parser.parser import ParserFactory

class ResourceLoader(builtins.object):
    """
    This class is used for loading the resources during application setup.

    - path:     the path to the resource file
    - session:  the Session object for local debugging
    """

    def __init__(self,
                 path: str,
                 session: Session):
        self.__path = path
        self.__session = session
        self.__content = None
        self.__resources = None

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, value):
        raise ValueError(f'{ResourceLoader.__name__}: path object cannot '
                         f'be set manually')

    def load_resources(self) -> bool:
        """
        This function opens the file at 'path', reads its content and
        closes the stream.
        """
        rf = None
        try:
            self.__session.debug_msg(f"{ResourceLoader.__name__}:"
                                     f" is opening the file")
            rf = open(self.__path, "r")
            self.__session.debug_msg(f"{ResourceLoader.__name__}: "
                                     f"file open successfully")
            self.__content = rf.read()
            self.__session.debug_msg(self.__content)
        except FileNotFoundError:
            raise SystemExit(f"{ResourceLoader.__name__}: no such file or "
                             f"directory '{self.__path}'")
        finally:
            if rf:
                self.__session.debug_msg(
                        f"{ResourceLoader.__name__}: "
                        f"is closing the file")
                rf.close()
        return True

    def parse_resources(self) -> bool:
        """This method parses the resources if content is not None,
        otherwise a SystemExit error is raised.

        A Parser object is obtained from the ParserFactory.
        If the file extension is not supported, then a TypeError is raised.
        """
        if self.__content is None:
            err_msg = f"{ResourceLoader.__name__}: " \
                      f"raw content is empty. You must call method " \
                      f"'{ResourceLoader.load_resources.__name__}' " \
                      f"before '{ResourceLoader.parse_resources.__name__}'."
            self.__session.debug_msg(err_msg)
            raise SystemExit(err_msg)

        try:
            parser = ParserFactory.make_parser_from_extension_file(
                    file_extension = self.__path.split('.')[-1],
                    raw_content = self.__content)
            self.__session.debug_msg(f"{ResourceLoader.__name__}: "
                                     f"parser created successfully: type "
                                     f"{parser.__class__.__name__}")
            self.__session.debug_msg(f"{ResourceLoader.__name__}:"
                                     f" try to parse resources")
            self.__resources = parser.parse()
            self.__session.debug_msg(f"{ResourceLoader.__name__}:"
                                     f" resources parsed successfully")
        except TypeError as terr:
            raise SystemExit(str(terr))
        return True

    def get_database_connection(self):
        pass

    def get_logger_config(self):
        pass


    def __str__(self):
        return f"{ResourceLoader.__name__}: " \
               f"\'path\'={self.__path}"
