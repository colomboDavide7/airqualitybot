#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 19:28
# @Description: this file defines a resource loader class
#
#################################################
import builtins


class ResourceLoader(builtins.object):

    def __init__(self, path):
        self.__path = path

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, value):
        raise ValueError('Path object cannot be changed')

