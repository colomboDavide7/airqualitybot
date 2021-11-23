######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 17:07
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List
import airquality.api.model.base as mdl


class BaseUniformModel(abc.ABC):
    pass


class ParamIDValue:

    def __init__(self, id_: int, value: str):
        self.id = id_
        self.value = value


class BaseAPI2DBAdapter(abc.ABC):

    @abc.abstractmethod
    def adapt(self, responses: List[mdl.BaseResponseModel]) -> List[BaseUniformModel]:
        pass
