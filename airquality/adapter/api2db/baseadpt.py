######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 17:07
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List
import airquality.api.model.baseresp as mdl


class BaseUniformModel(abc.ABC):
    pass


class BaseAPI2DBAdapter(abc.ABC):

    @abc.abstractmethod
    def adapt(self, responses: List[mdl.BaseResponseModel]) -> List[BaseUniformModel]:
        pass
