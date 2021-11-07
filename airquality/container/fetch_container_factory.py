######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 07/11/21 10:59
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
from airquality.container.fetch_container import FetchContainer


class FetchContainerFactory:

    def __init__(self, fetch_container_class=FetchContainer):
        self.fetch_container_class = fetch_container_class

    def make_container(self, parameters: Dict[str, Any]):
        return self.fetch_container_class(parameters=parameters)
