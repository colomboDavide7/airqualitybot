#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 19:28
# @Description: this file defines a resource loader class
#
#################################################
import builtins

from airquality.app.session import Session


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

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, value):
        raise ValueError('Path object cannot be changed')

    def open_read_close(self) -> bool:
        """
        This function opens the file at 'path', reads its content and
        closes the stream.
        :rtype: object
        """
        rf = None
        try:
            self.__session.debug_msg("ResourceLoader is opening the file")
            rf = open(self.__path, "r")
            self.__session.debug_msg("File open successfully")
            content = rf.read()
            self.__session.debug_msg(content)
        except FileNotFoundError as err:
            raise SystemExit(str(err))
        finally:
            if rf:
                self.__session.debug_msg("ResourceLoader is closing the file")
                rf.close()
        return True

    # def __get_parser_from_extension(self, file_ext):
    #     if file_ext == 'json':
    #         print("JSON parser")
    #     elif file_ext == 'xml':
    #         print("XML parser")
    #     elif file_ext == 'txt':
    #         print("TXT parser")
    #     else:
    #         print("invalid extension file")

    def __str__(self):
        return "resource path: {p}".format(p=self.__path)
