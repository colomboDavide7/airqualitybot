######################################################
#
# Author: Davide Colombo
# Date: 08/12/21 19:11
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List
import airquality.source.abc as basesource
import airquality.source.api.resp.abc as resptype
import airquality.source.api.api_req as request


# ------------------------------- APISourceABC ------------------------------- #
class APISourceABC(basesource.SourceABC, abc.ABC):

    def __init__(self, api_request: request.APIRequest, log_filename="log"):
        super(APISourceABC, self).__init__(log_filename=log_filename)
        self.api_request = api_request

    @abc.abstractmethod
    def get(self) -> List[resptype.APIRespTypeABC]:
        pass
