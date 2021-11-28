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
import airquality.api.url.baseurl as url


class Command(log.Loggable, abc.ABC):

    def __init__(self, ub: url.BaseURLBuilder, fw: apiwrp.FetchWrapper, log_filename="log"):
        super(Command, self).__init__(log_filename=log_filename)
        self.url_builder = ub
        self.fetch_wrapper = fw

    @abc.abstractmethod
    def execute(self):
        pass
