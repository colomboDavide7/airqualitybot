######################################################
#
# Author: Davide Colombo
# Date: 22/11/21 19:04
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List
import airquality.database.util.datatype.timestamp as ts
import airquality.database.util.postgis.geom as geo
import container.measure.param.param_id_val as par_c


class MeasureContainer(abc.ABC):

    def __init__(self, record_id: int, timestamp: ts.Timestamp, parameters: List[par_c.ParamIDValueContainer]):
        self.record_id = record_id
        self.timestamp = timestamp
        self.parameters = parameters


class MeasureContainerWithGeom(MeasureContainer):

    def __init__(
            self,
            record_id: int,
            timestamp: ts.Timestamp,
            parameters: List[par_c.ParamIDValueContainer],
            postgis_geom: geo.PostgisGeometry
    ):
        super(MeasureContainerWithGeom, self).__init__(record_id=record_id, timestamp=timestamp, parameters=parameters)
        self.postgis_geom = postgis_geom
