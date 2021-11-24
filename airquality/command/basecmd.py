######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 12:03
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.logger.loggable as log
import airquality.api.fetchwrp as apiwrp
import airquality.database.op.ins.ins as ins


class Command(log.Loggable, abc.ABC):

    ################################ __init__ ###############################
    def __init__(
            self, fw: apiwrp.FetchWrapper, iw: ins.InsertWrapper, log_filename="log"
    ):
        super(Command, self).__init__(log_filename=log_filename)
        self.fetch_wrapper = fw
        self.insert_wrapper = iw

    ################################ execute ###############################
    @abc.abstractmethod
    def execute(self):
        pass
