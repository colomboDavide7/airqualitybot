######################################################
#
# Author: Davide Colombo
# Date: 14/11/21 16:40
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict, Any
import airquality.logger.loggable as log
import airquality.api.fetchwrp as apiwrp


class DateLooper(log.Loggable):

    def __init__(self, fetch_wrapper: apiwrp.FetchWrapper, log_filename="app"):
        super(DateLooper, self).__init__(log_filename=log_filename)
        self.fetch_wrapper = fetch_wrapper

    def update_url_param(self, param2update: Dict[str, Any]):
        self.fetch_wrapper.add_database_api_param(param2update)

    def set_channel_name(self, channel_name: str):
        self.fetch_wrapper.set_channel_name(channel_name)

    @abc.abstractmethod
    def has_next(self) -> bool:
        pass

    @abc.abstractmethod
    def get_next_sensor_data(self) -> List[Dict[str, Any]]:
        pass

    @abc.abstractmethod
    def _get_next_date_url_param(self) -> Dict[str, Any]:
        pass
