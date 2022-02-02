######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 12:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from unittest import TestCase, main
from airquality.datamodel.fromdb import SensorApiParamDM


def _last_acquisition_test_datetime():
    return datetime.strptime("2018-12-11 18:49:00", "%Y-%m-%d %H:%M:%S")


def _sensor_api_param_test_datamodel():
    return SensorApiParamDM(
            sensor_id=1,
            api_key="fakekey",
            api_id="fakeident",
            ch_name="fakename",
            last_acquisition=_last_acquisition_test_datetime()
        )


class TestAPIParamDataclass(TestCase):

    def test_apiparam_dataclass(self):
        api_param = _sensor_api_param_test_datamodel()
        self.assertEqual(api_param.sensor_id, 1)
        self.assertEqual(api_param.api_key, "fakekey")
        self.assertEqual(api_param.api_id, "fakeident")
        self.assertEqual(api_param.ch_name, "fakename")
        self.assertEqual(api_param.last_acquisition, _last_acquisition_test_datetime())


if __name__ == '__main__':
    main()
