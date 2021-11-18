######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 13/11/21 15:56
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.adapter.config as c
import airquality.adapter.api2db.sensor as sens
import airquality.database.util.postgis.geom as geom
import airquality.database.util.datatype.timestamp as ts


class TestSensorAdapter(unittest.TestCase):

    def setUp(self) -> None:
        self.purpleair_adapter = sens.get_sensor_adapter('purpleair',
                                                         postgis_class=geom.PointBuilder,
                                                         timestamp_class=ts.UnixTimestamp)

    def test_get_sensor_reshaper_class(self):
        self.assertEqual(self.purpleair_adapter.__class__, sens.PurpleairSensorAdapter)

        with self.assertRaises(SystemExit):
            sens.get_sensor_adapter('bad sensor type')

    def test_successfully_reshape_purpleair_sensor_data(self):
        test_packet = {'name': 'n1', 'sensor_index': 'idx1',
                       'latitude': 'lat_val', 'longitude': 'lng_val',
                       'primary_id_a': 'id1A', 'primary_id_b': 'id1B', 'primary_key_a': 'key1A',
                       'primary_key_b': 'key1B',
                       'secondary_id_a': 'id2A', 'secondary_id_b': 'id2B', 'secondary_key_a': 'key2A',
                       'secondary_key_b': 'key2B',
                       'date_created': 'd'}

        expected_output = {c.SENS_NAME: 'n1 (idx1)',
                           c.SENS_INFO: [
                               {c.SENS_CH: c.FST_CH_A, c.TIMEST: {c.CLS: ts.UnixTimestamp, c.KW: {'timestamp': 'd'}}},
                               {c.SENS_CH: c.FST_CH_B, c.TIMEST: {c.CLS: ts.UnixTimestamp, c.KW: {'timestamp': 'd'}}},
                               {c.SENS_CH: c.SND_CH_A, c.TIMEST: {c.CLS: ts.UnixTimestamp, c.KW: {'timestamp': 'd'}}},
                               {c.SENS_CH: c.SND_CH_B, c.TIMEST: {c.CLS: ts.UnixTimestamp, c.KW: {'timestamp': 'd'}}}],
                           c.SENS_GEOM: {c.CLS: geom.PointBuilder, c.KW: {'lat': 'lat_val', 'lng': 'lng_val'}},
                           c.TIMEST: {c.CLS: ts.CurrentTimestamp, c.KW: {}},
                           c.SENS_PARAM: [{c.PAR_NAME: 'primary_id_a', c.PAR_VAL: 'id1A'},
                                          {c.PAR_NAME: 'primary_id_b', c.PAR_VAL: 'id1B'},
                                          {c.PAR_NAME: 'primary_key_a', c.PAR_VAL: 'key1A'},
                                          {c.PAR_NAME: 'primary_key_b', c.PAR_VAL: 'key1B'},
                                          {c.PAR_NAME: 'secondary_id_a', c.PAR_VAL: 'id2A'},
                                          {c.PAR_NAME: 'secondary_id_b', c.PAR_VAL: 'id2B'},
                                          {c.PAR_NAME: 'secondary_key_a', c.PAR_VAL: 'key2A'},
                                          {c.PAR_NAME: 'secondary_key_b', c.PAR_VAL: 'key2B'}],
                           c.SENS_TYPE: 'PurpleAir/ThingSpeak'}
        actual_output = self.purpleair_adapter.reshape(test_packet)
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_purpleair_api_param(self):
        test_missing_api_param = {'name': 'n1', 'sensor_index': 'idx1',
                                  'primary_id_a': 'id1A', 'primary_id_b': 'id1B', 'primary_key_a': 'key1A',
                                  'secondary_id_a': 'id2A', 'secondary_id_b': 'id2B', 'secondary_key_a': 'key2A'}
        with self.assertRaises(SystemExit):
            self.purpleair_adapter.reshape(test_missing_api_param)

    def test_exit_on_missing_sensor_name(self):
        test_missing_name = {'latitude': 'lat_val', 'longitude': 'lng_val',
                             'primary_id_a': 'id1A', 'primary_id_b': 'id1B', 'primary_key_a': 'key1A',
                             'primary_key_b': 'key1B',
                             'secondary_id_a': 'id2A', 'secondary_id_b': 'id2B', 'secondary_key_a': 'key2A',
                             'secondary_key_b': 'key2B', 'date_created': 'd'}
        with self.assertRaises(SystemExit):
            self.purpleair_adapter.reshape(test_missing_name)

    def test_exit_on_missing_geolocation(self):
        test_missing_geom = {'name': 'n1', 'sensor_index': 'idx1',
                             'primary_id_a': 'id1A', 'primary_id_b': 'id1B', 'primary_key_a': 'key1A',
                             'primary_key_b': 'key1B',
                             'secondary_id_a': 'id2A', 'secondary_id_b': 'id2B', 'secondary_key_a': 'key2A',
                             'secondary_key_b': 'key2B', 'date_created': 'd'}
        with self.assertRaises(SystemExit):
            self.purpleair_adapter.reshape(test_missing_geom)

    def test_exit_on_missing_date_created(self):
        test_missing_date_created = {'name': 'n1', 'sensor_index': 'idx1', 'latitude': 'lat_val',
                                     'longitude': 'lng_val',
                                     'primary_id_a': 'id1A', 'primary_id_b': 'id1B', 'primary_key_a': 'key1A',
                                     'primary_key_b': 'key1B',
                                     'secondary_id_a': 'id2A', 'secondary_id_b': 'id2B', 'secondary_key_a': 'key2A',
                                     'secondary_key_b': 'key2B'}
        with self.assertRaises(SystemExit):
            self.purpleair_adapter.reshape(test_missing_date_created)

    def test_exit_on_missing_api_param(self):
        test_packet = {'name': 'n1', 'sensor_index': 'idx1', 'latitude': 'lat_val', 'longitude': 'lng_val',
                       'primary_id_b': 'id1B', 'primary_key_a': 'key1A',
                       'primary_key_b': 'key1B',
                       'secondary_id_a': 'id2A', 'secondary_id_b': 'id2B', 'secondary_key_a': 'key2A',
                       'secondary_key_b': 'key2B', 'date_created': 'd'}
        with self.assertRaises(SystemExit):
            self.purpleair_adapter.reshape(test_packet)


if __name__ == '__main__':
    unittest.main()
