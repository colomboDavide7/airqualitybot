######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 05/11/21 11:44
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
from airquality.container.sql_container import SQLContainer, SQLContainerComposition


################################ CONTAINER FACTORY ################################
class InitializeContainerFactory(object):

    def __init__(self, container_class=None):
        self.container_class = container_class

    def make_container(self, packets: List[Dict[str, Any]], sensor_id: int) -> SQLContainer:

        containers = []
        temp_sensor_id = sensor_id
        for packet in packets:
            containers.append(self.container_class(sensor_id=temp_sensor_id, packet=packet))
            temp_sensor_id += 1
        return SQLContainerComposition(containers=containers)
