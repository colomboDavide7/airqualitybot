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
class SQLContainerFactory(object):

    def __init__(self, container_class=None):
        self.container_class = container_class

    def make_container_with_start_sensor_id(self, packets: List[Dict[str, Any]], start_sensor_id: int) -> SQLContainer:

        containers = []
        temp_sensor_id = start_sensor_id
        for packet in packets:
            containers.append(self.container_class(sensor_id=temp_sensor_id, packet=packet))
            temp_sensor_id += 1
        return SQLContainerComposition(containers=containers)

    def make_container_by_mapping_sensor_id(self, packets: List[Dict[str, Any]], sensorname2id_map: Dict[str, Any]
                                            ) -> SQLContainer:
        # In this method, we are also doing a filter operation on the packets !!!
        sensor_names = sensorname2id_map.keys()
        containers = []
        for packet in packets:
            sensor_name = packet['name']
            if sensor_name in sensor_names:
                sensor_id = sensorname2id_map[sensor_name]
                containers.append(self.container_class(sensor_id=sensor_id, packet=packet))
        return SQLContainerComposition(containers=containers)

    def make_container_with_sensor_id(self, packets: List[Dict[str, Any]], sensor_id: int):
        containers = []
        for packet in packets:
            containers.append(self.container_class(sensor_id=sensor_id, packet=packet))
        return SQLContainerComposition(containers=containers)
