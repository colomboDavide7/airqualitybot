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
from airquality.container.sql_container_factory import InitializeContainer


@dataclass
class SensorSQLWrapper(SQLWrapperPacket):
    container: InitializeContainer

    def sql(self) -> str:
        return f"('{self.container.sensor_type}', '{self.container.database_sensor_name}')"
