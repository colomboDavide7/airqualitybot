######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 16:35
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.datamodel.request import AddFixedSensorRequest, AddMobileMeasureRequest, Channel
from airquality.datamodel.geometry import PostgisPoint, NullGeometry
from airquality.core.iteritems import IterableItemsABC
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
            created_at = datetime.fromtimestamp(dm.date_created)
            channels = [
                Channel(api_key=dm.primary_key_a, api_id=str(dm.primary_id_a), channel_name="1A", last_acquisition=created_at),
                Channel(api_key=dm.primary_key_b, api_id=str(dm.primary_id_b), channel_name="1B", last_acquisition=created_at),
                Channel(api_key=dm.secondary_key_a, api_id=str(dm.secondary_id_a), channel_name="2A", last_acquisition=created_at),
                Channel(api_key=dm.secondary_key_b, api_id=str(dm.secondary_id_b), channel_name="2B", last_acquisition=created_at)
            ]
            yield AddFixedSensorRequest(
                type="Purpleair/Thingspeak",
                name=f"{dm.name} ({dm.sensor_index})",
                channels=channels,
                geolocation=PostgisPoint(latitude=dm.latitude, longitude=dm.longitude)
            )


class AddAtmotubeMeasureRequestBuilder(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules for translating
    a set of *AtmotubeDatamodel* items into an *AddMobileMeasureRequest* Generator.
    """

    TIMESTAMP_FMT = "%Y-%m-%dT%H:%M:%S.000Z"

    def __init__(self, datamodel: IterableItemsABC, code2id: Dict[str, int]):
        self.datamodel = datamodel
        self.code2id = code2id

    def items(self) -> Generator[AddMobileMeasureRequest, None, None]:
        for dm in self.datamodel:
            pt = dm.coords
            yield AddMobileMeasureRequest(
                timestamp=datetime.strptime(dm.time, self.TIMESTAMP_FMT),
                geolocation=NullGeometry() if pt is None else PostgisPoint(latitude=pt['lat'], longitude=pt['lon']),
                measures=[(ident, getattr(dm, code)) for code, ident in self.code2id.items() if getattr(dm, code) is not None]
            )
