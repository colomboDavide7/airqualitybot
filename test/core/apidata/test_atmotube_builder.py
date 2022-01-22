# ======================================
# @author:  Davide Colombo
# @date:    2022-01-22, sab, 15:47
# ======================================
import test._test_utils as tutils
from unittest import TestCase, main
from airquality.core.apidata_builder import AtmotubeAPIDataBuilder


def _test_atmotube_api_json_response():
    return tutils.get_json_response_from_file(
        filename='atmotube_response.json'
    )


class TestAtmotubeAPIDataBuilder(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._builder = AtmotubeAPIDataBuilder(
            json_response=_test_atmotube_api_json_response()
        )

# =========== TEST METHODS
    def test_create_atmotube_datamodel(self):
        self.assertEqual(len(self._builder), 2)
        self._assert_built_data()
        self._assert_index_error(index=2)
        self._assert_index_error(index=-3)

# =========== SUPPORT METHODS
    def _assert_index_error(self, index):
        with self.assertRaises(IndexError):
            self._builder[index]

    def _assert_built_data(self):
        datamodel = self._builder[0]
        self.assertEqual(datamodel.time, "2021-08-10T23:59:00.000Z")
        self.assertEqual(datamodel.voc, 0.17)
        self.assertEqual(datamodel.pm1, 8)
        self.assertEqual(datamodel.pm25, 10)
        self.assertEqual(datamodel.pm10, 11)
        self.assertEqual(datamodel.t, 29)
        self.assertEqual(datamodel.h, 42)
        self.assertEqual(datamodel.p, 1004.68)


if __name__ == '__main__':
    main()
