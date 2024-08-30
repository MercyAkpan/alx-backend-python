#!/usr/bin/env python3
"""
This modules contains tests for client.py file.
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
import client


class TestGithubOrgClient(unittest.TestCase):
    """
    This is a class to test the GithubOrgClient class.
    """
    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    # I imported the get_json from client.py to patch it in the test method
    @patch.object(client, 'get_json')
    def test_org(self, company, mock_get):
        """
        This test memoization and mocking in the org method of GithubOrgClient.
        """
        mock_response = Mock()
        mock_response.return_value = company
        mock_get.return_value = mock_response
        # Creates an instance of the GithubOrgClient class
        organization = client.GithubOrgClient(company)
        # print(organization)
        # I got the full htpps url of the Organisation
        url_name = (organization.ORG_URL.format(org=company))
        # Called the org method twice to show memoization
        result1 = organization.org()
        result2 = organization.org()
        # See if the mock_get (get_json) is truly called once.
        mock_get.assert_called_once_with(url_name)
        # Check if the results are equal to the company_name
        self.assertEqual(result1, company)
        self.assertEqual(result2, company)
