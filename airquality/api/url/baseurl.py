######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:36
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc


class BaseURLBuilder(abc.ABC):

    def __init__(self, url_template: str):
        self.url_template = url_template
        self.fmt = None

    def with_api_response_fmt(self, fmt: str):
        self.fmt = fmt
        return self

    @abc.abstractmethod
    def build(self) -> str:
        pass
