######################################################
#
# Author: Davide Colombo
# Date: 27/12/21 19:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.atmotube import Atmotube
from airquality.dblookup import SensorAPIParam

SQL_DATETIME_FMT = "%Y-%m-%d %H:%M:%S"


class TestAtmotube(TestCase):

    @property
    def test_url_template(self) -> str:
        return "some_address?api_key={api_key}&mac={api_id}&format={api_fmt}&date={date}"

    @property
    def test_personality(self) -> str:
        return "some_personality"

    @property
    def test_apiparam(self):
        return [('id1', 'sens1', 'k1', 'i1', 'n1', datetime.strptime("2021-10-11 09:44:00", SQL_DATETIME_FMT)),
                ('id2', 'sens1', 'k2', 'i2', 'n2', datetime.strptime("2021-10-11 09:45:00", SQL_DATETIME_FMT)),
                ('id3', 'sens2', 'k3', 'i3', 'n3', datetime.strptime("2021-10-18 17:18:00", SQL_DATETIME_FMT))]

    @property
    def expected_apiparam(self):
        return {SensorAPIParam(pkey='id1', sensor_id='sens1', ch_key='k1', ch_id='i1', ch_name='n1',
                               last_acquisition=datetime.strptime("2021-10-11 09:44:00", SQL_DATETIME_FMT)),
                SensorAPIParam(pkey='id2', sensor_id='sens1', ch_key='k2', ch_id='i2', ch_name='n2',
                               last_acquisition=datetime.strptime("2021-10-11 09:45:00", SQL_DATETIME_FMT)),
                SensorAPIParam(pkey='id3', sensor_id='sens2', ch_key='k3', ch_id='i3', ch_name='n3',
                               last_acquisition=datetime.strptime("2021-10-18 17:18:00", SQL_DATETIME_FMT))
                }

    # def test_start_record_id(self):
    #     mocked_adapter = MagicMock()
    #     mocked_adapter.fetch_one.return_value = (None,)
    #     atmotube = Atmotube(personality=self.test_personality, url_template=self.test_url_template, dbadapter=mocked_adapter)
    #     self.assertEqual(atmotube.start_record_id, 1)
    #
    # def test_atmotube_apiparam(self):
    #     mocked_adapter = MagicMock()
    #     mocked_adapter.fetch_all.return_value = self.test_apiparam
    #     atmotube = Atmotube(personality=self.test_personality, url_template=self.test_url_template, dbadapter=mocked_adapter)
    #     self.assertEqual(atmotube.apiparam, self.expected_apiparam)


if __name__ == '__main__':
    main()
