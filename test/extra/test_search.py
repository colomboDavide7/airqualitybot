# ======================================
# @author:  Davide Colombo
# @date:    2022-02-2, mer, 11:23
# ======================================
from unittest import TestCase, main
from airquality.extra.weather_extra import _nested_search_dict


class TestSearch(TestCase):

    def test_nested_dict_search(self):
        test_keywords = ['k3', 'kk2', 'kkk1']
        test_source = {'k1': 'v1', 'k2': 'v2', 'k3': {'kk1': 'vv1', 'kk2': {'kkk1': 'vvv1'}}}
        actual = _nested_search_dict(
            source=test_source,
            keywords=test_keywords
        )
        self.assertEqual(actual, 'vvv1')

    def test_nested_dict_search_with_searched_value_equal_to_none(self):
        test_keywords = ['k3', 'kk2', 'kkk2']
        test_source = {'k1': 'v1', 'k2': 'v2', 'k3': {'kk1': 'vv1', 'kk2': {'kkk1': 'vvv1', 'kkk2': None}}}
        actual = _nested_search_dict(
            source=test_source,
            keywords=test_keywords
        )
        self.assertIsNone(actual)

    def test_raise_key_error_if_wrong_keyword_path_is_passed(self):
        test_keywords = ['k3', 'kk2', 'kkk2']
        test_source = {'k1': 'v1', 'k2': 'v2', 'k3': {'kk1': 'vv1', 'kk2': {'kkk1': 'vvv1'}}}
        actual = _nested_search_dict(source=test_source, keywords=test_keywords)
        self.assertIsNone(actual)


if __name__ == '__main__':
    main()
