# ======================================
# @author:  Davide Colombo
# @date:    2022-01-20, gio, 20:34
# ======================================
from datetime import datetime
from unittest import TestCase, main
from airquality.datamodel.requests import Channel
from airquality.datamodel.geometry import PostgisPoint
from airquality.datamodel.requests import AddFixedSensorRequest


def _sensor_channel_test_data():
    ts = datetime.fromtimestamp(1234567890)
    return [
        Channel(api_key="k1", api_id="1", channel_name="fakename1", last_acquisition=ts),
        Channel(api_key="k2", api_id="2", channel_name="fakename2", last_acquisition=ts),
        Channel(api_key="k3", api_id="3", channel_name="fakename3", last_acquisition=ts),
        Channel(api_key="k4", api_id="4", channel_name="fakename4", last_acquisition=ts)
    ]


def _sensor_location_test_data():
    return PostgisPoint(latitude=10.99, longitude=-36.88)


def _expected_last_acquisition_timestamp() -> datetime:
    return datetime(2009, 2, 14, 0, 31, 30)


def _expected_geom_from_text():
    return "ST_GeomFromText('POINT(-36.88 10.99)', 4326)"


class TestAddPurpleairSensorRequest(TestCase):

# =========== TEST METHODS
    def test_request_for_adding_fixed_sensor(self):
        request = AddFixedSensorRequest(
            type="faketype",
            name="fakename",
            channels=_sensor_channel_test_data()
        )
        self.assertEqual(request.type, "faketype")
        self.assertEqual(request.name, "fakename")
        self._assert_channels(request.channels)

# =========== SUPPORT METHODS
    def _assert_channels(self, channels):
        ts = _expected_last_acquisition_timestamp()
        self._assert_channel_data(channel=channels[0], ident='1', key='k1', name='fakename1', ts=ts)
        self._assert_channel_data(channel=channels[1], ident='2', key='k2', name='fakename2', ts=ts)
        self._assert_channel_data(channel=channels[2], ident='3', key='k3', name='fakename3', ts=ts)
        self._assert_channel_data(channel=channels[3], ident='4', key='k4', name='fakename4', ts=ts)

    def _assert_channel_data(self, channel: Channel, ident: str, key: str, name: str, ts: datetime):
        self.assertEqual(channel.api_id, ident)
        self.assertEqual(channel.api_key, key)
        self.assertEqual(channel.channel_name, name)
        self.assertEqual(channel.last_acquisition, ts)


if __name__ == '__main__':
    main()
