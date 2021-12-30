######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 20:12
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from json import loads
from typing import Generator
from itertools import islice
from abc import abstractmethod
from urllib.request import urlopen
from collections.abc import Iterable
from airquality.request import AddPurpleairSensorRequest, AddAtmotubeMeasureRequest


class InputBoundaryInterface(Iterable):
    """
    An *Iterable* that represents the input boundary interface for isolating the communication with *input_device(s)*
    """

    @abstractmethod
    def get_requests(self):
        pass

    def __getitem__(self, index):
        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError(f"{type(self).__name__} expected '{index}' to be in [0 - {len(self)}]")
        return next(islice(self, index, None))

    def __iter__(self):
        return self.get_requests()

    def __len__(self):
        return sum(1 for _ in self.get_requests())


class AddPurpleairSensorRequestBuilder(InputBoundaryInterface):
    """
    An *InputBoundaryInterface* that fetches data from Purpleair API and return a Generator of requests.
    """

    def __init__(self, url: str):
        with urlopen(url) as http_response:
            parsed = loads(http_response.read())
            self.fields = parsed['fields']
            self.data = parsed['data']

    def get_requests(self) -> Generator[AddPurpleairSensorRequest, None, None]:
        return (AddPurpleairSensorRequest(**(dict(zip(self.fields, data)))) for data in self.data)


class AddAtmotubeMeasureRequestBuilder(InputBoundaryInterface):
    """
    An *InputBoundaryInterface* that fetches data from Atmotube API and return a Generator o requests.
    """
    def __init__(self, url: str):
        with urlopen(url) as http_response:
            parsed = loads(http_response.read())
            self.items = parsed['data']['items']

    def get_requests(self) -> Generator[AddAtmotubeMeasureRequest, None, None]:
        return (AddAtmotubeMeasureRequest(**item) for item in self.items)
