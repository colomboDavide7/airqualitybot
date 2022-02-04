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
            sid=1,
            key="fakekey",
            id="fakeident",
            ch="fakename",
            last=_last_acquisition_test_datetime()
        )


class TestAPIParamDataclass(TestCase):

    def test_apiparam_dataclass(self):
        api_param = _sensor_api_param_test_datamodel()
        self.assertEqual(api_param.sid, 1)
        self.assertEqual(api_param.key, "fakekey")
        self.assertEqual(api_param.id, "fakeident")
        self.assertEqual(api_param.ch, "fakename")
        self.assertEqual(api_param.last, _last_acquisition_test_datetime())


if __name__ == '__main__':
    main()
