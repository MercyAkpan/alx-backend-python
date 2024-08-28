#!/usr/bin/env python3
import utils 
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
import requests

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
        self.assertEqual(utils.access_nested_map(nested_map, path), expected_output)

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
            >>You should check the below first because it verifies that mock_get was used correctly.
            If this assertion fails, it means the get_json function did not call mock_get as expected
            and the subsequent assertion about the result may be irrelevant.
        """
        mock_get.assert_called_once_with(test_url)
        """
        >> If the mock interaction is correct, then you can be more confident 
            that any failure in the result assertion 
            is related to the function’s logic or result handling.
        """
        self.assertEqual(result, test_payload)


    if __name__ == "__main__":
        unittest.main()
