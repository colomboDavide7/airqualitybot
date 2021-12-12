######################################################
#
# Author: Davide Colombo
# Date: 12/12/21 09:32
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.database.record.abc as recabc
import airquality.api.resp.abc as resptype
import airquality.types.timestamp as tstype


class InfoRecordType(recabc.RecordTypeABC):

    def __init__(self, response: resptype.InfoAPIRespTypeABC):
        self.response = response

    def sensor_record(self, sensor_id: int) -> str:
        return f"({sensor_id}, '{self.response.sensor_type()}', '{self.response.sensor_name()}'),"

    def apiparam_record(self, sensor_id: int) -> str:
        timestamp = self.response.date_created().ts
        return ','.join(f"({sensor_id}, '{c.key}', '{c.ident}', '{c.name}', '{timestamp}')" for c in self.response.channels()) + ','

    def geolocation_record(self, sensor_id: int) -> str:
        timestamp = tstype.CurrentTimestamp().ts
        geom = self.response.geolocation().geom_from_text()
        return f"({sensor_id}, '{timestamp}', {geom}),"


class InfoRecordBuilder(recabc.RecordBuilderABC):

    def build(self, data: List[resptype.InfoAPIRespTypeABC]) -> List[InfoRecordType]:
        return [InfoRecordType(response=r) for r in data]
