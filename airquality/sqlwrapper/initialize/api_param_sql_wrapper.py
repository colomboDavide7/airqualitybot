######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 16:13
# Description: this script defines an Abstract Base Class called APIParamPacket that extends the Packet class.
#              The purpose of this class and its subclasses is to define the behavior for converting data fetched from
#              API into a sql statement for inserting data into the database.
#
######################################################
from dataclasses import dataclass
from airquality.sqlwrapper.sql_wrapper_packet import SQLWrapperPacket
from airquality.container.initialize_container_factory import InitializeContainer

# USE A FOR CYCLE FOR ADDING ALL THE PARAMETERS BECAUSE THEY CAN VARY BASED ON FIELDS DEFINED IN THE 'api.json' FILE BY THE USER!!!


@dataclass
class APIParamSQLWrapper(SQLWrapperPacket):
    sensor_id: int
    container: InitializeContainer

    def sql(self) -> str:
        query = ""
        for api_param in self.container.api_param_container:
            query += f"({self.sensor_id}, '{api_param.param_name}', '{api_param.param_value}'),"
        return query.strip(',')


# class SQLWrapperAPIPacketPurpleair(SQLWrapperAPIPacket):
#
#     def __init__(self, sensor_id: int, packet: PlainAPIPacketPurpleair):
#         super().__init__(sensor_id)
#         self.packet = packet
#
#     def sql(self) -> str:
#         query = ""
#         query += f"({self.sensor_id}, 'primary_id_a', '{self.packet.primary_id_a}'),"
#         query += f"({self.sensor_id}, 'primary_key_a', '{self.packet.primary_key_a}'),"
#         query += f"({self.sensor_id}, 'primary_timestamp_a', null),"
#         query += f"({self.sensor_id}, 'primary_id_b', '{self.packet.primary_id_b}'),"
#         query += f"({self.sensor_id}, 'primary_key_b', '{self.packet.primary_key_b}'),"
#         query += f"({self.sensor_id}, 'primary_timestamp_b', null),"
#         query += f"({self.sensor_id}, 'secondary_id_a', '{self.packet.secondary_id_a}'),"
#         query += f"({self.sensor_id}, 'secondary_key_a', '{self.packet.secondary_key_a}'),"
#         query += f"({self.sensor_id}, 'secondary_timestamp_a', null),"
#         query += f"({self.sensor_id}, 'secondary_id_b', '{self.packet.secondary_id_b}'),"
#         query += f"({self.sensor_id}, 'secondary_key_b', '{self.packet.secondary_key_b}'),"
#         query += f"({self.sensor_id}, 'secondary_timestamp_b', null)"
#         return query
#
#     def __str__(self):
#         return f"primary_id_a={self.packet.primary_id_a}, primary_key_a={self.packet.primary_key_a}, " \
#                f"primary_id_b={self.packet.primary_id_b}, primary_key_b={self.packet.primary_key_b}, " \
#                f"secondary_id_a={self.packet.secondary_id_a}, secondary_key_a={self.packet.secondary_key_a}, " \
#                f"secondary_id_b={self.packet.secondary_id_b}, secondary_key_b={self.packet.secondary_key_b}, " \
#                f"primary_timestamp_a=null, primary_timestamp_b=null, secondary_timestamp_a=null, " \
#                f"secondary_timestamp_b=null"
