######################################################
#
# Author: Davide Colombo
# Date: 22/12/21 20:24
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from collections import namedtuple
from typing import Dict


class SensorAPIParam(namedtuple('SensorAPIParam', ['pkey', 'sensor_id', 'ch_key', 'ch_id', 'ch_name', 'last_acquisition'])):
    """
    A class that wraps a database lookup to *sensor_api_param* table just to avoid using list indexing and make the
    code more explicit.
    """

    @property
    def database_url_param(self) -> Dict[str, str]:
        return {'api_key': self.ch_key, 'api_id': self.ch_id}

    def __repr__(self):
        return f"{type(self).__name__}(pkey={self.pkey}, sensor_id='{self.sensor_id}', api_key=XXX, " \
               f"api_id=XXX, ch_name='{self.ch_name}', last_activity={self.last_acquisition})"
