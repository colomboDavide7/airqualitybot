######################################################
#
# Author: Davide Colombo
# Date: 01/01/22 11:06
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.usecase.add_places import AddPlaces


class TestAddPlaces(TestCase):

    @patch('airquality.usecase.add_places.listdir')
    @patch('airquality.usecase.add_places.isfile')
    @patch('airquality.core.apidata_builder.open')
    def test_run_add_fixed_sensors_usecase(self, mocked_open, mocked_isfile, mocked_listdir):
        mocked_listdir.return_value = {"fakefile1.txt", ".ignored_file"}
        mocked_isfile.return_value = [True, True, True]

        mocked_gateway = MagicMock()
        mocked_gateway.insert_places = MagicMock()
        mocked_gateway.get_service_id_from_name.return_value = 133
        mocked_gateway.get_poscodes_of_country.return_value = {'p1', 'p2', 'p3'}

        with open('test_resources/ES.txt', 'r') as f:
            content = f.read()

        mocked_responses = MagicMock()
        mocked_responses.read.side_effect = [content]
        mocked_responses.__enter__.return_value = mocked_responses
        mocked_open.return_value = mocked_responses

        runner = AddPlaces(output_gateway=mocked_gateway, input_dir_path="fake_path")
        self.assertIn('fakefile1.txt', runner.filenames)
        self.assertNotIn('.ignored_file', runner.filenames)

        self.assertEqual(runner.service_id, 133)

        self.assertIn('p1', runner.poscodes_of("fakecountry"))
        self.assertIn('p2', runner.poscodes_of("fakecountry"))
        self.assertIn('p3', runner.poscodes_of("fakecountry"))

        self.assertEqual(runner.fullpath("fakefile.txt"), "fake_path/fakefile.txt")

        runner.run()
        responses = mocked_gateway.insert_places.call_args[0][0]
        self.assertEqual(len(responses), 3)

        resp = responses[0]
        expected_place_record = "(133, '04001', 'ES', 'Almeria', 'Almeria', 'Andalucia', ST_GeomFromText('POINT(-2.4597 36.8381)', 4326))"
        self.assertEqual(resp.place_record, expected_place_record)


if __name__ == '__main__':
    main()
