######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 16:35
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.request import AddFixedSensorRequest, AddMobileMeasureRequest, Channel, Geolocation
from airquality.iteritems import IterableItemsABC
from typing import Dict, Generator
from datetime import datetime


class AddPurpleairSensorRequestBuilder(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules for translating
    a set of *PurpleairDatamodel* items into an *AddFixedSensorRequest* Generator.
    """

    def __init__(self, datamodel: IterableItemsABC):
        self.datamodel = datamodel

    def items(self) -> Generator[AddFixedSensorRequest, None, None]:
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


class AddAtmotubeMeasureRequestBuilder(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules for translating
    a set of *AtmotubeDatamodel* items into an *AddMobileMeasureRequest* Generator.
    """

    ATMOTUBE_TIMESTAMP_FMT = "%Y-%m-%dT%H:%M:%S.000Z"

    def __init__(self, datamodel: IterableItemsABC, code2id: Dict[str, int]):
        self.datamodel = datamodel
        self.code2id = code2id

    def items(self) -> Generator[AddMobileMeasureRequest, None, None]:
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
