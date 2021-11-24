######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 13/11/21 15:56
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.to_delete.config as adapt_const
import database.ext.config as geom_conf
import database.dtype.config as time_conf
import container.sensor as sens
import database.ext.postgis as geom
import database.dtype.timestamp as ts


class TestSensorAdapter(unittest.TestCase):

    def setUp(self) -> None:
        self.purpleair_adapter = sens.get_sensor_adapter('purpleair',
                                                         postgis_class=geom.PostgisPoint,
                                                         timestamp_class=ts.UnixTimestamp)

    def test_get_sensor_reshaper_class(self):
        self.assertEqual(self.purpleair_adapter.__class__, sens.PurpleairSensorContainerBuilder)

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

        expected_output = {adapt_const.SENS_NAME: 'n1 (idx1)',
                           adapt_const.SENS_INFO: [
                               {adapt_const.SENS_CH: adapt_const.FST_CH_A,
                                adapt_const.TIMEST: {adapt_const.CLS: ts.UnixTimestamp,
                                                     adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: 'd'}}},
                               {adapt_const.SENS_CH: adapt_const.FST_CH_B,
                                adapt_const.TIMEST: {adapt_const.CLS: ts.UnixTimestamp,
                                                     adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: 'd'}}},
                               {adapt_const.SENS_CH: adapt_const.SND_CH_A,
                                adapt_const.TIMEST: {adapt_const.CLS: ts.UnixTimestamp,
                                                     adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: 'd'}}},
                               {adapt_const.SENS_CH: adapt_const.SND_CH_B,
                                adapt_const.TIMEST: {adapt_const.CLS: ts.UnixTimestamp,
                                                     adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: 'd'}}}],
                           adapt_const.SENS_GEOM: {adapt_const.CLS: geom.PostgisPoint,
                                                   adapt_const.KW: {geom_conf.POINT_INIT_LAT_NAME: 'lat_val',
                                                                    geom_conf.POINT_INIT_LNG_NAME: 'lng_val'}},
                           adapt_const.TIMEST: {adapt_const.CLS: ts.CurrentTimestamp, adapt_const.KW: {}},
                           adapt_const.SENS_PARAM: [{adapt_const.PAR_NAME: 'primary_id_a', adapt_const.PAR_VAL: 'id1A'},
                                                    {adapt_const.PAR_NAME: 'primary_id_b', adapt_const.PAR_VAL: 'id1B'},
                                                    {adapt_const.PAR_NAME: 'primary_key_a', adapt_const.PAR_VAL: 'key1A'},
                                                    {adapt_const.PAR_NAME: 'primary_key_b', adapt_const.PAR_VAL: 'key1B'},
                                                    {adapt_const.PAR_NAME: 'secondary_id_a', adapt_const.PAR_VAL: 'id2A'},
                                                    {adapt_const.PAR_NAME: 'secondary_id_b', adapt_const.PAR_VAL: 'id2B'},
                                                    {adapt_const.PAR_NAME: 'secondary_key_a', adapt_const.PAR_VAL: 'key2A'},
                                                    {adapt_const.PAR_NAME: 'secondary_key_b', adapt_const.PAR_VAL: 'key2B'}],
                           adapt_const.SENS_TYPE: 'PurpleAir/ThingSpeak'}
        actual_output = self.purpleair_adapter.uniform(test_packet)
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_purpleair_api_param(self):
        test_missing_api_param = {'name': 'n1', 'sensor_index': 'idx1',
                                  'primary_id_a': 'id1A', 'primary_id_b': 'id1B', 'primary_key_a': 'key1A',
                                  'secondary_id_a': 'id2A', 'secondary_id_b': 'id2B', 'secondary_key_a': 'key2A'}
        with self.assertRaises(SystemExit):
            self.purpleair_adapter.uniform(test_missing_api_param)

    def test_exit_on_missing_sensor_name(self):
        test_missing_name = {'latitude': 'lat_val', 'longitude': 'lng_val',
                             'primary_id_a': 'id1A', 'primary_id_b': 'id1B', 'primary_key_a': 'key1A', 'primary_key_b': 'key1B',
                             'secondary_id_a': 'id2A', 'secondary_id_b': 'id2B', 'secondary_key_a': 'key2A', 'secondary_key_b': 'key2B',
                             'date_created': 'd'}
        with self.assertRaises(SystemExit):
            self.purpleair_adapter.uniform(test_missing_name)

    def test_exit_on_missing_geolocation(self):
        test_missing_geom = {'name': 'n1', 'sensor_index': 'idx1',
                             'primary_id_a': 'id1A', 'primary_id_b': 'id1B', 'primary_key_a': 'key1A',
                             'primary_key_b': 'key1B',
                             'secondary_id_a': 'id2A', 'secondary_id_b': 'id2B', 'secondary_key_a': 'key2A',
                             'secondary_key_b': 'key2B', 'date_created': 'd'}
        with self.assertRaises(SystemExit):
            self.purpleair_adapter.uniform(test_missing_geom)

    def test_exit_on_missing_date_created(self):
        test_missing_date_created = {'name': 'n1', 'sensor_index': 'idx1', 'latitude': 'lat_val',
                                     'longitude': 'lng_val',
                                     'primary_id_a': 'id1A', 'primary_id_b': 'id1B', 'primary_key_a': 'key1A',
                                     'primary_key_b': 'key1B',
                                     'secondary_id_a': 'id2A', 'secondary_id_b': 'id2B', 'secondary_key_a': 'key2A',
                                     'secondary_key_b': 'key2B'}
        with self.assertRaises(SystemExit):
            self.purpleair_adapter.uniform(test_missing_date_created)

    def test_exit_on_missing_api_param(self):
        test_packet = {'name': 'n1', 'sensor_index': 'idx1', 'latitude': 'lat_val', 'longitude': 'lng_val',
                       'primary_id_b': 'id1B', 'primary_key_a': 'key1A',
                       'primary_key_b': 'key1B',
                       'secondary_id_a': 'id2A', 'secondary_id_b': 'id2B', 'secondary_key_a': 'key2A',
                       'secondary_key_b': 'key2B', 'date_created': 'd'}
        with self.assertRaises(SystemExit):
            self.purpleair_adapter.uniform(test_packet)


if __name__ == '__main__':
    unittest.main()
