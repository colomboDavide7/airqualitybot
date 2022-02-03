# ======================================
# @author:  Davide Colombo
# @date:    2022-02-3, gio, 15:00
# ======================================
from unittest import TestCase, main
import airquality.extra.string as string


def _test_char_to_remove():
    return [
        ' ',
        '.',
        '-'
    ]


class TestStringExtraFunction(TestCase):

    def test_name_cleaner_1(self):
        test_name = 'DICAr - P@P-PA-1 (13027)'
        self.assertEqual(
            string.string_cleaner(test_name, char2remove=_test_char_to_remove()),
            'dicarp@ppa1(13027)'
        )

    def test_name_cleaner_2(self):
        test_name = 'P.za Marelli - P@P-PA-35 (16821)'
        self.assertEqual(
            string.string_cleaner(test_name, char2remove=_test_char_to_remove()),
            'pzamarellip@ppa35(16821)'
        )

    def test_name_cleaner_with_simple_name(self):
        test_name = 'Atmotube Pro (Lisbon 2)'
        self.assertEqual(
            string.string_cleaner(test_name, char2remove=_test_char_to_remove()),
            'atmotubepro(lisbon2)'
        )

    def test_number_cleaner(self):
        self.assertEqual(
            string.literalize_number(9.123456),
            '9dot12346'
        )

    def test_negative_number_cleaner(self):
        self.assertEqual(
            string.literalize_number(number=-74.198),
            "minus74dot19800"
        )


if __name__ == '__main__':
    main()
