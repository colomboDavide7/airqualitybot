######################################################
#
# Author: Davide Colombo
# Date: 24/11/21 09:57
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.database.record.baserec as base
import airquality.adapter.api2db.updtadapt.updtadapt as updtadapt


class UpdateRecord(base.BaseRecord):

    def __init__(self):
        pass


class UpdateRecordBuilder(base.BaseRecordBuilder):

    def record(self, sensor_data: List[updtadapt.UpdateUniformModel], sensor_id: int = None) -> UpdateRecord:
        pass
