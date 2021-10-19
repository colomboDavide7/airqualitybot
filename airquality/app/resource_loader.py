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
                 session: Session,
                 path: str):
        self.__path = path

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
        """
        rf = None
        try:
            rf = open(self.__path, "r")
            content = rf.read()
            print(content)
        except Exception as ex:
            print(str(ex))
        finally:
            if rf:
                rf.close()
        return True


    def __str__(self):
        return "resource path: {p}".format(p=self.__path)
