######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 16:35
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.request import AddFixedSensorRequest, AddMobileMeasureRequest, Channel, Geolocation
from airquality.datamodel_builder import PurpleairDatamodelBuilder, AtmotubeDatamodelBuilder
from collections.abc import Iterable
from typing import Dict, Generator
from abc import abstractmethod
from datetime import datetime
from itertools import islice


class RequestBuilder(Iterable):
    """
    An *Iterable* that represents the interface for building system requests.
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


class AddPurpleairSensorRequestBuilder(RequestBuilder):
    """
    A *RequestBuilder* that defines how an *AddFixedSensorRequest* is created.
    """

    def __init__(self, datamodel: PurpleairDatamodelBuilder):
        self.datamodel = datamodel

    def get_requests(self) -> Generator[AddFixedSensorRequest, None, None]:
        for dm in self.datamodel:
            last_acquisition = datetime.fromtimestamp(dm.date_created)
            channels = [
                Channel(api_key=dm.primary_key_a, api_id=str(dm.primary_id_a), channel_name="1A", last_acquisition=last_acquisition),
                Channel(api_key=dm.primary_key_b, api_id=str(dm.primary_id_b), channel_name="1B", last_acquisition=last_acquisition),
                Channel(api_key=dm.secondary_key_a, api_id=str(dm.secondary_id_a), channel_name="2A", last_acquisition=last_acquisition),
                Channel(api_key=dm.secondary_key_b, api_id=str(dm.secondary_id_b), channel_name="2B", last_acquisition=last_acquisition)
            ]

            geolocation = Geolocation(latitude=dm.latitude, longitude=dm.longitude)
            name = f"{dm.name} ({dm.sensor_index})"

            yield AddFixedSensorRequest(type="Purpleair/Thingspeak", name=name, channels=channels, geolocation=geolocation)


class AddAtmotubeMeasureRequestBuilder(RequestBuilder):
    """
    A *RequestBuilder* that defines how an *AddMobileMeasureRequest* is created.
    """

    ATMOTUBE_TIMESTAMP_FMT = "%Y-%m-%dT%H:%M:%S.000Z"

    def __init__(self, datamodel: AtmotubeDatamodelBuilder, code2id: Dict[str, int]):
        self.datamodel = datamodel
        self.code2id = code2id

    def get_requests(self) -> Generator[AddMobileMeasureRequest, None, None]:
        for dm in self.datamodel:
            coords = dm.coords
            geolocation = Geolocation(latitude=coords['lat'], longitude=coords['lon'])
            timestamp = datetime.strptime(dm.time, self.ATMOTUBE_TIMESTAMP_FMT)

            measures = [
                (self.code2id['voc'], dm.voc),
                (self.code2id['pm1'], dm.pm1),
                (self.code2id['pm25'], dm.pm25),
                (self.code2id['pm10'], dm.pm10),
                (self.code2id['t'], dm.t),
                (self.code2id['h'], dm.h),
                (self.code2id['p'], dm.p)
            ]

            yield AddMobileMeasureRequest(timestamp=timestamp, geolocation=geolocation, measures=measures)
