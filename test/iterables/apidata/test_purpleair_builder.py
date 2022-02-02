# ======================================
# @author:  Davide Colombo
# @date:    2022-01-22, sab, 15:37
# ======================================
import test._test_utils as tutils
from unittest import TestCase, main
from airquality.iterables.fromapi import PurpleairIterableDatamodels


def _test_purpleair_api_json_response():
    return tutils.get_json_response_from_file(
        filename='purpleair_response.json'
    )


class TestPurpleairAPIDataBuilder(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._builder = PurpleairIterableDatamodels(
            json_response=_test_purpleair_api_json_response()
        )

# =========== TEST METHOD
    def test_create_purpleair_datamodel(self):
        self.assertEqual(len(self._builder), 3)
        self._assert_built_data()
        self._assert_index_error(index=3)
        self._assert_index_error(index=-4)

# =========== SUPPORT METHODS
    def _assert_index_error(self, index):
        with self.assertRaises(IndexError):
            self._builder[index]

    def _assert_built_data(self):
        datamodel = self._builder[0]
        self.assertEqual(datamodel.name, "n1")
        self.assertEqual(datamodel.sensor_index, 1)
        self.assertEqual(datamodel.primary_id_a, 111)
        self.assertEqual(datamodel.primary_key_a, "key1a1")
        self.assertEqual(datamodel.primary_id_b, 112)
        self.assertEqual(datamodel.primary_key_b, "key1b1")
        self.assertEqual(datamodel.secondary_id_a, 113)
        self.assertEqual(datamodel.secondary_key_a, "key2a1")
        self.assertEqual(datamodel.secondary_id_b, 114)
        self.assertEqual(datamodel.secondary_key_b, "key2b1")
        self.assertEqual(datamodel.date_created, 1531432748)


if __name__ == '__main__':
    main()
