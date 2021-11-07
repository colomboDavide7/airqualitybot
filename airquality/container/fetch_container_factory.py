######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 07/11/21 10:59
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
from airquality.container.fetch_container import FetchContainer


class FetchContainerFactory:

    def __init__(self, fetch_container_class=FetchContainer):
        self.fetch_container_class = fetch_container_class

    def make_container(self, parameters: List[Dict[str, Any]]) -> List[FetchContainer]:
        containers = []
        for param in parameters:
            containers.append(self.fetch_container_class(param))
        return containers
