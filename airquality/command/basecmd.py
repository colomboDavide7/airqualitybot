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
import airquality.database.op.ins.ins as insertoprt
import airquality.database.op.sel.sensor as sel_type


class Command(log.Loggable, abc.ABC):

    ################################ __init__ ###############################
    def __init__(
            self, fw: apiwrp.FetchWrapper, iw: insertoprt.InsertWrapper, stw: sel_type.TypeSelectWrapper, log_filename="log"
    ):
        super(Command, self).__init__(log_filename=log_filename)
        self.fetch_wrapper = fw
        self.insert_wrapper = iw
        self.select_type_wrapper = stw

    ################################ execute ###############################
    @abc.abstractmethod
    def execute(self):
        pass
