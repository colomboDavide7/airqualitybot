######################################################
#
# Author: Davide Colombo
# Date: 10/12/21 18:38
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Generator
from urllib.request import urlopen
from urllib.error import URLError
import api.deprecated_fmt as urlabc


# ------------------------------- APIRepo ------------------------------- #
class APIRepo(object):

    def __init__(self, url_builder: urlabc.URLFormatter):
        self.url_builder = url_builder

    ################################ read_all() ################################
    def read_all(self) -> Generator[str, None, None]:
        try:
            all_urls = self.url_builder
            for url in all_urls:
                yield urlopen(url).read()
        except (URLError, ValueError) as err:
            raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} exception => {err!r}")
