######################################################
#
# Author: Davide Colombo
# Date: 26/11/21 11:39
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Dict, Any, List
import source.api.resp.base as base
import airquality.types.apiresp.measresp as resp


class MeasureAPIRespBuilder(base.APIRespBuilder, abc.ABC):

    def __init__(self, timestamp_cls):
        self.timestamp_cls = timestamp_cls
        self.channel_name = None

    @abc.abstractmethod
    def get_measures(self, item: Dict[str, Any]) -> List[resp.ParamNameValue]:
        pass

    def with_channel_name(self, channel_name: str):
        self.channel_name = channel_name
        return self

    def exit_on_missing_channel_name(self):
        if self.channel_name is None:
            raise SystemExit(f"{MeasureAPIRespBuilder.__name__}: bad builder setup => missing required 'channel_name'")
