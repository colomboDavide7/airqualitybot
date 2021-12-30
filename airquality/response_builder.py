######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 16:35
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.request import AddPurpleairSensorRequest, AddAtmotubeMeasureRequest
from airquality.response import AddFixedSensorResponse, AddMobileMeasureResponse, Channel, Geolocation
from datetime import datetime
from typing import Dict


class AddPurpleairSensorResponseBuilder(object):

    def __init__(self, request: AddPurpleairSensorRequest):
        self.request = request

    def build_response(self) -> AddFixedSensorResponse:
        last_acquisition = datetime.fromtimestamp(self.request.date_created)
        channels = [
            Channel(api_key=self.request.primary_key_a, api_id=str(self.request.primary_id_a), channel_name="1A",
                    last_acquisition=last_acquisition),
            Channel(api_key=self.request.primary_key_b, api_id=str(self.request.primary_id_b), channel_name="1B",
                    last_acquisition=last_acquisition),
            Channel(api_key=self.request.secondary_key_a, api_id=str(self.request.secondary_id_a), channel_name="2A",
                    last_acquisition=last_acquisition),
            Channel(api_key=self.request.secondary_key_b, api_id=str(self.request.secondary_id_b), channel_name="2B",
                    last_acquisition=last_acquisition),
        ]

        geolocation = Geolocation(latitude=self.request.latitude, longitude=self.request.longitude)
        name = f"{self.request.name} ({self.request.sensor_index})"
        return AddFixedSensorResponse(
            type="Purpleair/Thingspeak", name=name, channels=channels, geolocation=geolocation
        )


class AddAtmotubeMeasureResponseBuilder(object):
    ATMOTUBE_TIMESTAMP_FMT = "%Y-%m-%dT%H:%M:%S.000Z"

    def __init__(self, request: AddAtmotubeMeasureRequest, code2id: Dict[str, int]):
        self.request = request
        self.code2id = code2id

    def build_response(self) -> AddMobileMeasureResponse:
        coords = self.request.coords
        geolocation = Geolocation(latitude=coords['lat'], longitude=coords['lon'])
        timestamp = datetime.strptime(self.request.time, self.ATMOTUBE_TIMESTAMP_FMT)

        measures = [
            (self.code2id['voc'], self.request.voc),
            (self.code2id['pm1'], self.request.pm1),
            (self.code2id['pm25'], self.request.pm25),
            (self.code2id['pm10'], self.request.pm10),
            (self.code2id['t'], self.request.t),
            (self.code2id['h'], self.request.h),
            (self.code2id['p'], self.request.p)
        ]

        return AddMobileMeasureResponse(
            timestamp=timestamp, geolocation=geolocation, measures=measures
        )
