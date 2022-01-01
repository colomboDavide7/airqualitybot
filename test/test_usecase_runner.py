######################################################
#
# Author: Davide Colombo
# Date: 01/01/22 11:06
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
# from unittest import TestCase, main
# from unittest.mock import MagicMock, patch
# from airquality.usecase_runner import AddFixedSensorsRunner
#
#
# class TestUsecaseRunner(TestCase):
#
#     @patch('airquality.database.adapter.connect')
#     def test_run_add_fixed_sensors_usecase(self, mocked_connect):
#         mocked_environment = MagicMock()
#         mocked_environment.dbname.return_value = "fakedbname"
#         mocked_environment.port.return_value = "fakeport"
#         mocked_environment.host.return_value = "fakehost"
#         mocked_environment.user.return_value = "fakeuser"
#         mocked_environment.password.return_value = "fakepassword"
#
#         mocked_conn = MagicMock()
#         mocked_connect.return_value = mocked_conn
#
#         runner = AddFixedSensorsRunner(env=mocked_environment, personality="fake_pers")
#
#
# if __name__ == '__main__':
#     main()
