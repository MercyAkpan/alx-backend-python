#!/usr/bin/env python3
import unittest 
from unittest.mock import patch, Mock
from parameterized import parameterized
import client 

class TestGithubOrgClient(unittest.TestCase):
    """
    This is a git
    """
    @parameterized.expand([
        ( "google", "google company"),
        ("abc", "abc company"),
    ])
    @patch.object(client, 'get_json')
    def test_org(self, company, company_name , mock_get):
        """
        """
        # with patch.object('get_json')
        mock_response = Mock()
        mock_response.return_value = company_name
        mock_get.return_value = mock_response

        organization = client.GithubOrgClient(company)
        # print(organization)
        url_name = (organization.ORG_URL.format(org=company))
        # print(url_name)
        result1 = organization.org()
        result2 = organization.org()
        # print(result)
        mock_get.assert_called_once_with(url_name)
        # print("hereeee")
        # print(result1)
        self.assertEqual(result1, company_name)
        self.assertEqual(result2, company_name)

