# ======================================
# @author:  Davide Colombo
# @date:    2022-01-23, dom, 12:40
# ======================================
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.datamodel.fromdb import SensorInfoDM
from airquality.extra.logging import FileHandlerRotator
from airquality.extra.logging import _custom_log_filename


def _test_sensor_identity():
    return SensorInfoDM(
        sensor_id=0,
        sensor_name='n1',
        sensor_lng=9,
        sensor_lat=10
    )


def _test_sensor_identity_2():
    return SensorInfoDM(
        sensor_id=1,
        sensor_name='n2'
    )


def _mocked_file_handler():
    mocked_filehandler = MagicMock()
    mocked_filehandler.setLevel = MagicMock()
    return mocked_filehandler


def _mocked_logger():
    mocked_l = MagicMock()
    mocked_l.removeHandler = MagicMock()
    return mocked_l


def _expected_filename() -> str:
    return "fake_dir/sensor_0_n1_10dot00000_9dot00000.log"


class TestFileHandlerRotator(TestCase):

    def setUp(self) -> None:
        self._rotator = FileHandlerRotator(
            logger_dir="fake_dir",
            logger_name="fake_name",
            logger_level="fake_level",
            logger_fmt="fake_fmt"
        )

    @patch('airquality.extra.logging.logging')
    def test_rotate_file_handler(self, mocked_logging):
        mocked_logging.FileHandler = MagicMock()
        mocked_logging.Formatter = MagicMock()
        mocked_logging.getLogger.return_value = _mocked_logger()
        mocked_logging.FileHandler.return_value = _mocked_file_handler()

        self._rotator.rotate(
            sensor_ident=_test_sensor_identity()
        )
        mocked_logging.FileHandler.assert_called_with(
            filename=_expected_filename()
        )
        mocked_logging.Formatter.assert_called_with(
            fmt='fake_fmt'
        )
        mocked_logging.FileHandler.return_value.setLevel.assert_called_with(
            level="fake_level"
        )

        self._rotator.rotate(
            sensor_ident=_test_sensor_identity_2()
        )

    def test_custom_log_filename_without_latitude_and_longitude(self):
        self.assertEqual(
            _custom_log_filename(sensor_id=0, sensor_name='n1'),
            'sensor_0_n1'
        )


if __name__ == '__main__':
    main()
