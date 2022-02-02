# ======================================
# @author:  Davide Colombo
# @date:    2022-01-22, sab, 15:52
# ======================================
import test._test_utils as tutils
from unittest import TestCase, main
from airquality.iterables.fromapi import ThingspeakIterableDatamodels


def _test_thingspeak_json_response():
    return tutils.get_json_response_from_file(
        filename='thingspeak_response_1A.json'
    )


class TestThingspeakAPIDataBuilder(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._builder = ThingspeakIterableDatamodels(
            json_response=_test_thingspeak_json_response()
        )

# =========== TEST METHODS
    def test_create_thingspeak_primary_channel_a_data(self):
        self.assertEqual(len(self._builder), 3)
        self._assert_built_data()
        self._assert_raise_index_error(index=3)
        self._assert_raise_index_error(index=-4)

# =========== SUPPORT METHODS
    def _assert_raise_index_error(self, index):
        with self.assertRaises(IndexError):
            self._builder[index]

    def _assert_built_data(self):
        datamodel = self._builder[0]
        self.assertEqual(datamodel.field1, 20.50)
        self.assertEqual(datamodel.field2, 35.53)
        self.assertEqual(datamodel.field3, 37.43)
        self.assertEqual(datamodel.field6, 55)
        self.assertEqual(datamodel.field7, 60)


if __name__ == '__main__':
    main()
