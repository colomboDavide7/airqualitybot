######################################################
#
# Author: Davide Colombo
# Date: 20/12/21 20:33
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from operator import itemgetter
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.sqldict import MutableSQLDict


TEST_DATABASE_RESPONSES = [("pkey1", "v1", "v2"), ("pkey2", "v3", "v4"), ("pkey3", "v5", "v6")]


class TestMutableSQLDict(TestCase):

    @property
    def mocked_table(self) -> MagicMock:
        mocked_table = MagicMock()
        mocked_table.join_cols.return_value = "joined cols"
        return mocked_table

    @property
    def mocked_adapter(self) -> MagicMock:
        mocked_adapter = MagicMock()
        mocked_adapter.fetch_all.return_value = map(itemgetter(0), TEST_DATABASE_RESPONSES)
        mocked_adapter.fetch_one.side_effect = TEST_DATABASE_RESPONSES
        return mocked_adapter

    def test_mutable_sqldict_delitem(self):
        key_to_delete = "bad_key_to_delete"
        mutable_dict = MutableSQLDict(table=self.mocked_table, dbadapter=self.mocked_adapter)
        with self.assertRaises(KeyError):
            del mutable_dict[key_to_delete]     # this line raises a KeyError if the key does not exist


if __name__ == '__main__':
    main()
