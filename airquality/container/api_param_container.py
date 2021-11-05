######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 05/11/21 10:58
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from dataclasses import dataclass
from airquality.container.container_to_sql import Container2SQL


@dataclass
class PurpleairAPIParamContainer(Container2SQL):
    sensor_id: int
    primary_id_a: str
    primary_id_b: str
    secondary_id_a: str
    secondary_id_b: str
    primary_key_a: str
    primary_key_b: str
    secondary_key_a: str
    secondary_key_b: str

    def container2sql(self) -> str:
        query = ""
        query += f"({self.sensor_id}, 'primary_id_a', '{self.primary_id_a}'),"
        query += f"({self.sensor_id}, 'primary_key_a', '{self.primary_key_a}'),"
        query += f"({self.sensor_id}, 'primary_timestamp_a', null),"
        query += f"({self.sensor_id}, 'primary_id_b', '{self.primary_id_b}'),"
        query += f"({self.sensor_id}, 'primary_key_b', '{self.primary_key_b}'),"
        query += f"({self.sensor_id}, 'primary_timestamp_b', null),"
        query += f"({self.sensor_id}, 'secondary_id_a', '{self.secondary_id_a}'),"
        query += f"({self.sensor_id}, 'secondary_key_a', '{self.secondary_key_a}'),"
        query += f"({self.sensor_id}, 'secondary_timestamp_a', null),"
        query += f"({self.sensor_id}, 'secondary_id_b', '{self.secondary_id_b}'),"
        query += f"({self.sensor_id}, 'secondary_key_b', '{self.secondary_key_b}'),"
        query += f"({self.sensor_id}, 'secondary_timestamp_b', null)"
        return query


@dataclass
class AtmotubeAPIParamContainer(Container2SQL):
    sensor_id: int
    api_key: str
    mac: str
    date: str

    def container2sql(self) -> str:
        query = ""
        query += f"({self.sensor_id}, 'api_key', '{self.api_key}'),"
        query += f"({self.sensor_id}, 'mac', '{self.mac}'),"
        query += f"({self.sensor_id}, 'date', '{self.date}')"
        return query
