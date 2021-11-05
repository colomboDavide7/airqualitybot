######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 17:16
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from dataclasses import dataclass
from airquality.sqlwrapper.sql_wrapper_packet import SQLWrapperPacket


@dataclass
class PurpleairSensorSQLWrapper(SQLWrapperPacket):
    database_sensor_name: str
    sensor_type: str

    def sql(self) -> str:
        return f"({self.sensor_type}', '{self.database_sensor_name}')"
