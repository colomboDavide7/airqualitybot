######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 20:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.api.url.dynurl as dyn
import airquality.database.dtype.timestamp as ts


class TimeURLBuilder(dyn.DynamicURLBuilder, abc.ABC):

    def __init__(self, target: dyn.DynamicURLBuilder, step_size_in_days: int = 1):
        super(TimeURLBuilder, self).__init__(address=target.address, options=target.options)
        self.target = target
        self.step_size_in_days = step_size_in_days
        self.start_ts = None
        self.stop_ts = None
        self.ended = False

    def with_start_ts(self, start: ts.SQLTimestamp):
        self.start_ts = start
        return self

    def with_stop_ts(self, stop: ts.SQLTimestamp):
        self.stop_ts = stop
        return self

    @abc.abstractmethod
    def get_next_date(self):
        pass

    def has_next_date(self):
        return not self.ended
