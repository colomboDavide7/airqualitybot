######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 10:13
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.logger.loggable as log


############################ FILE OBJECT BASE CLASS #############################
class StructuredFile(log.Loggable, abc.ABC):

    def __init__(self, log_filename="log"):
        super(StructuredFile, self).__init__(log_filename=log_filename)
