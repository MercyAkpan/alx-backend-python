#!/usr/bin/env python3
"""
This module contains the test cases for the utils module
"""
from utils import memoize
import utils
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
import requests
# import test_utils


class TestAccessNestedMap(unittest.TestCase):
    """
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected_output):
        """
        """
        self.assertEqual(utils.access_nested_map(
            nested_map, path), expected_output)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        """
        with self.assertRaises(KeyError):
            utils.access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        """
        mock_reponse = Mock()
        mock_reponse.json.return_value = test_payload
        mock_get.return_value = mock_reponse

        result = utils.get_json(test_url)
        """
        You should check `below` first because it verifies that mock_get
        was used correctly.If this assertion fails, it means the get_json
        function did not call mock_get as expected
        and the subsequent assertion about the result may be irrelevant.
        """
        mock_get.assert_called_once_with(test_url)
        """
        >> If the mock interaction is correct, then you can be more confident
            that any failure in the result assertion
            is related to the function’s logic or result handling.
        """
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    This class tests the memoize decorator
    """
    # print(dir(test_utils))
    # @patch.object(TestMemoize,'a_method',wraps=None)
    def test_memoize(self):
        """
        This method tests the memoize decorator
        """
        class TestClass():
            """
            This class tests the memoize decorator
            """
            def a_method(self):
                """
                This method tests the memoize decorator
                """
                return 42

            @memoize
            def a_property(self):
                """
                This method tests the memoize decorator
                """
                return self.a_method()
        with patch.object(TestClass, 'a_method')as mock_get:
            mock_response = Mock()
            mock_response.return_value = 42
            mock_get.return_value = mock_response
            result = TestClass()
            result1 = result.a_property()
            result2 = result.a_property()
            mock_get.assert_called_once()
            self.assertEqual(result1, mock_response.return_value)
            self.assertEqual(result2, mock_response.return_value)


if __name__ == "__main__":
    unittest.main()
