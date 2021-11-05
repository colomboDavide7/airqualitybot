######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 05/11/21 11:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from dataclasses import dataclass
from airquality.container.container_to_sql import Container2SQL


@dataclass
class PurpleairSensorContainer(Container2SQL):
    name: str
    sensor_index: str

    @property
    def database_sensor_name(self):
        return f"{self.name} ({self.sensor_index})"

    @property
    def sensor_type(self):
        return 'purpleair'

    def container2sql(self) -> str:
        return f"'{self.sensor_type}', '{self.database_sensor_name}'"
