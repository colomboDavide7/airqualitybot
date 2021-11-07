######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 07/11/21 10:25
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
from abc import ABC, abstractmethod


class FetchContainer(ABC):

    def __init__(self, parameters: Dict[str, Any]):
        self.id_name = parameters['channel_id']['name']
        self.id_val = parameters['channel_id']['val']
        self.key_name = parameters['channel_key']['name']
        self.key_val = parameters['channel_key']['val']
        self.ts_name = parameters['channel_ts']['name']
        self.ts_val = parameters['channel_ts']['val']

    @abstractmethod
    def url(self, api_address: str, optional_param: Dict[str, Any]) -> str:
        pass


class ChannelContainer(FetchContainer):

    def __init__(self, parameters: Dict[str, Any]):
        super().__init__(parameters)

    def url(self, api_address: str, optional_param: Dict[str, Any]) -> str:
        querystring = api_address + '?'
        querystring += self.id_name + '=' + self.id_val + '&'
        querystring += self.key_name + '=' + self.key_val + '&'
        querystring += self.ts_name + '=' + self.ts_val + '&'
        if optional_param:
            for key, val in optional_param.items():
                querystring += key + '=' + val + '&'
        return querystring.strip('&').replace(' ', '%20')


class ChannelContainerWithFormattableAddress(FetchContainer):

    def __init__(self, parameters: Dict[str, Any]):
        super().__init__(parameters)

    def url(self, api_address: str, optional_param: Dict[str, Any]) -> str:
        querystring = api_address.format(self.id_val) + '?'
        querystring += self.key_name + '=' + self.key_val + '&'
        querystring += self.ts_name + '=' + self.ts_val + '&'
        if optional_param:
            for key, val in optional_param.items():
                querystring += key + '=' + val + '&'
        return querystring.strip('&').replace(' ', '%20')
