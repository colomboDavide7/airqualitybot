######################################################
#
# Author: Davide Colombo
# Date: 20/12/21 20:07
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.sqldict import FrozenSQLDict

TEST_DATABASE_RESPONSES = [("pkey1", "v1", "v2"), ("pkey2", "v3", "v4"), ("pkey3", "v5", "v6")]


class TestSQLDict(TestCase):

    @property
    def mocked_table(self) -> MagicMock:
        mocked_table = MagicMock()
        mocked_table.join_cols.return_value = "joined cols"
        return mocked_table

    @property
    def mocked_adapter(self) -> MagicMock:
        mocked_adapter = MagicMock()
        mocked_adapter.fetch_all.return_value = TEST_DATABASE_RESPONSES
        mocked_adapter.fetch_one.side_effect = TEST_DATABASE_RESPONSES
        mocked_adapter.execute.return_value = True
        return mocked_adapter

    @property
    def mocked_len_adapter(self) -> MagicMock:
        mocked_adapter = self.mocked_adapter
        mocked_adapter.fetch_one.side_effect = [(3, )]
        return mocked_adapter

    def test_frozen_sqldict_getitem(self):
        frozen_dict = FrozenSQLDict(table=self.mocked_table, dbadapter=self.mocked_adapter)
        self.assertEqual(frozen_dict[0], TEST_DATABASE_RESPONSES[0])
        self.assertEqual(frozen_dict[1], TEST_DATABASE_RESPONSES[1])
        self.assertEqual(frozen_dict[2], TEST_DATABASE_RESPONSES[2])

    def test_frozen_sqldict_iter(self):
        frozen_dict = FrozenSQLDict(table=self.mocked_table, dbadapter=self.mocked_adapter)
        index = 0
        for row in frozen_dict:
            self.assertEqual(row, TEST_DATABASE_RESPONSES[index][0])
            index += 1

    def test_frozen_sqldict_len(self):
        frozen_dict = FrozenSQLDict(table=self.mocked_table, dbadapter=self.mocked_len_adapter)
        self.assertEqual(len(frozen_dict), len(TEST_DATABASE_RESPONSES))


if __name__ == '__main__':
    main()
