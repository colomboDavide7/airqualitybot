######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:36
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc


# ------------------------------- URLBuilderABC ------------------------------- #
class URLBuilderABC(abc.ABC):

    def __init__(self, url_template: str):
        self.url_template = url_template

    @abc.abstractmethod
    def build(self) -> str:
        pass
