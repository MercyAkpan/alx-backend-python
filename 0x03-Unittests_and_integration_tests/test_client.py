#!/usr/bin/env python3
"""
Unit Testing for GithubOrgClient Class

This module provides a set of unit tests for the `GithubOrgClient` class
from the `client` module. The tests are designed to verify the correct
functionality of the methods in `GithubOrgClient` that interact with
the GitHub API to fetch organization data.

The `parameterized` library is used to run the same test function with
different sets of input data, ensuring a wide range of scenarios are covered.
The `unittest.mock.patch` function is utilized to mock external dependencies
like network calls to the GitHub API, allowing tests to run without actual
network access.
"""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from requests.exceptions import HTTPError


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for the `GithubOrgClient` class.

    This test class covers various scenarios for the `org` method,
    which fetches organization details from GitHub. The tests ensure
    that the method correctly calls the external API, handles different
    inputs, and manages exceptions appropriately.
    """

    # @parameterized.expand([
    #     ("google", {"login": "google"}),
    #     ("abc", {"login": "abc"})
    # ])
    # @patch('client.get_json')
    # def test_org(self, org, expected, mock_get_json):
    #     """
    #     Test the `org` method of `GithubOrgClient`.

    #     This test verifies that the `org` property of the `GithubOrgClient`
    #     correctly returns the expected organization data. It uses the
    #     `parameterized` decorator to run the test multiple times with
    #     different inputs.

    #     Args:
    #         org (str): The name of the organization to retrieve.
    #         expected (Dict[str, Any]): The expected dictionary returned by
    #         `get_json`.
    #         mock_get_json (Any): The mocked `get_json` function.

    #     Asserts:
    #         - The returned organization matches the expected dictionary.
    #         - `get_json` is called with the correct URL.
    #     """
    #     mock_get_json.return_value = expected

    #     client = GithubOrgClient(org)
    #     organisation = client.org

    #     url = client.ORG_URL.format(org=org)

    #     self.assertEqual(organisation, expected)
    #     mock_get_json.assert_called_once_with(url)

    @parameterized.expand(
            [
                ("google",),
                ("abc",),
            ]
        )
    @patch("client.get_json")
    def test_org(self, org_name, mock_org):
        """Method ot test"""
        client = GithubOrgClient(org_name)
        mock_org.return_value = {"login": org_name}
        self.assertEqual(client.org, mock_org.return_value)
        mock_org.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """
        Test the `_public_repos_url` property of `GithubOrgClient`.

        This test ensures that the `_public_repos_url` property correctly
        returns the public repositories URL for a given organization by
        accessing the `org` property.

        It uses `unittest.mock.PropertyMock` to mock the `org` property to
        return a predefined payload containing the `repos_url`. The test then
        checks that `_public_repos_url` extracts this URL correctly.

        Asserts:
            - The returned value from `_public_repos_url` matches the
              `repos_url` from the mocked `org` property.
            - The `org` property is accessed exactly once.
        """
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock
        ) as mock_org:
            payload = {"repos_url": "https://api.github.com/orgs/google/repos"}
            mock_org.return_value = payload

            client = GithubOrgClient("google")
            result = client._public_repos_url

            self.assertEqual(result, payload["repos_url"])
            mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, get_json):
        """
        Test the `public_repos` method of `GithubOrgClient`.

        This test ensures that the `public_repos` method correctly returns
        a list of public repository names for a given organization.

        It mocks the `get_json` function to return a predefined payload of
        repositories and the `_public_repos_url` property to provide the URL
        to fetch these repositories.

        Args:
            get_json (Mock): Mocked `get_json` function.

        Asserts:
            - The returned list from `public_repos` matches the names of
              repositories in the mocked response.
            - The `_public_repos_url` property is accessed exactly once.
            - The `get_json` function is called exactly once.
        """
        test_payload = {
            'repos_url': "https://api.github.com/users/microsoft/repos",
            'repos': [
                {
                    "id": 123456,
                    "name": "vscode",
                    "private": False,
                    "owner": {
                        "login": "microsoft",
                        "id": 12345,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/microsoft/vscode",
                    "created_at": "2015-01-01T00:00:00Z",
                    "updated_at": "2020-01-01T00:00:00Z",
                    "has_issues": True,
                    "forks": 100,
                    "default_branch": "main",
                },
                {
                    "id": 789012,
                    "name": "TypeScript",
                    "private": False,
                    "owner": {
                        "login": "microsoft",
                        "id": 12345,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/microsoft/TypeScript",
                    "created_at": "2012-01-01T00:00:00Z",
                    "updated_at": "2020-01-01T00:00:00Z",
                    "has_issues": True,
                    "forks": 200,
                    "default_branch": "main",
                },
            ]
        }

        get_json.return_value = test_payload["repos"]
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_payload["repos_url"]
            self.assertEqual(
                GithubOrgClient("microsoft").public_repos(),
                ["vscode", "TypeScript"],
            )
            mock_public_repos_url.assert_called_once()
        get_json.assert_called_once()

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo, license_key, expected):
        """
        Test the `has_license` method of `GithubOrgClient`.

        This test checks whether the `has_license` method correctly identifies
        if a repository contains the specified license key.

        Args:
            repo (Dict[str, Any]): Repository dictionary containing license
            information.
            license_key (str): License key to search for.
            expected (bool): Expected result indicating whether the license key
            should be present.

        Asserts:
            - The result of `has_license` matches the expected value.
        """
        client = GithubOrgClient("test_org")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class(
    [
        {
            'org_payload': TEST_PAYLOAD[0][0],
            'repos_payload': TEST_PAYLOAD[0][1],
            'expected_repos': TEST_PAYLOAD[0][2],
            'apache2_repos': TEST_PAYLOAD[0][3],
        },
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for the `GithubOrgClient` class.

    This test class verifies the correct functionality of methods in the
    `GithubOrgClient` class when interacting with the GitHub API. The tests
    cover scenarios including fetching public repositories and filtering
    repositories by license.

    Attributes:
        org_payload (Dict[str, Any]): The payload returned when querying
            the organization's details.
        repos_payload (List[Dict[str, Any]]): The payload returned when
            querying the organization's repositories.
        expected_repos (List[str]): The expected list of repository names.
        apache2_repos (List[str]): The expected list of repository names
            with Apache 2.0 license.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up the test environment by patching the `requests.get` method
        to return predefined payloads for specific URLs.

        This method creates a mock `requests.get` function that returns
        different responses based on the requested URL.
        """
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """
        Test the `public_repos` method of `GithubOrgClient`.

        This test checks that the `public_repos` method returns the expected
        list of repository names for a given organization.
        """
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """
        Test the `public_repos` method with a license filter.

        This test checks that the `public_repos` method correctly filters
        repositories by the specified license.
        """
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Clean up the test environment by stopping the patcher for
        `requests.get`.
        """
        cls.get_patcher.stop()
