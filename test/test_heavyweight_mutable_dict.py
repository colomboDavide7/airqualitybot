######################################################
#
# Author: Davide Colombo
# Date: 21/12/21 08:58
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.sqldict import HeavyweightInsertSQLDict


class TestHeavyweightMutableSQLDict(TestCase):

    @property
    def mocked_table(self) -> MagicMock:
        mocked_table = MagicMock()
        mocked_table.join_cols.return_value = "joined cols"
        return mocked_table

    @property
    def mocked_adapter(self) -> MagicMock:
        mocked_adapter = MagicMock()
        mocked_adapter.fetch_one.return_value = 3
        return mocked_adapter

    def test_commit_empty_values_raises_ValueError(self):
        heavyweight_dict = HeavyweightInsertSQLDict(table=self.mocked_table, dbadapter=self.mocked_adapter)
        with self.assertRaises(ValueError):
            heavyweight_dict.commit(values="")


if __name__ == '__main__':
    main()
