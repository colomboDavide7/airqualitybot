######################################################
#
# Author: Davide Colombo
# Date: 22/12/21 20:24
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from collections import namedtuple


MEASURE_PARAM_COLS = ['param_code', 'param_name', 'param_unit']


class MeasureParamLookup(namedtuple('MeasureParamLookup', MEASURE_PARAM_COLS)):
    """A class that wraps a database lookup to 'measure_param' table just to avoid using list indexing."""

    def __repr__(self):
        return f"{type(self).__name__}(param_code={self.param_code}, param_name={self.param_name}, param_unit={self.param_unit})"
