######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 12:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from unittest import TestCase, main
from airquality.apiparam import APIParam


class TestAPIParamDataclass(TestCase):

    def test_apiparam_dataclass(self):
        test_last_acquisition = datetime.strptime("2018-12-11 18:49:00", "%Y-%m-%d %H:%M:%S")
        data = APIParam(
            sensor_id=1,
            api_key="fakekey",
            api_id="fakeident",
            ch_name="fakename",
            last_acquisition=test_last_acquisition
        )

        self.assertEqual(data.sensor_id, 1)
        self.assertEqual(data.api_key, "fakekey")
        self.assertEqual(data.api_id, "fakeident")
        self.assertEqual(data.ch_name, "fakename")
        self.assertEqual(data.last_acquisition, test_last_acquisition)
        expected_repr = "APIParam(sensor_id=1, api_key=XXX, api_id=XXX, ch_name=fakename, last_acquisition=2018-12-11 18:49:00)"
        self.assertEqual(repr(data), expected_repr)


if __name__ == '__main__':
    main()
