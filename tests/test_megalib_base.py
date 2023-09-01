from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, mock_open
from os import environ

from megadebrid.libs.base import MegaDebrid


class TestMegaDebridApi(IsolatedAsyncioTestCase):
    """
    Test all methods of MegaDebrid base library
    """

    @patch(
        "builtins.open",
        mock_open(read_data=open("tests/config.ini", "r", encoding="utf-8").read()),
    )
    async def test_configparser(self):
        """
        Test read configs from 'tests/config.ini'
        """
        async with MegaDebrid() as megadebrid:
            # Read CREDENTIALS from 'tests/config.ini'
            self.assertEqual(megadebrid.config.get_credentials()["Username"], "user")
            self.assertEqual(
                megadebrid.config.get_credentials()["Password"], "password"
            )
            # Read COOKIES PHPSESSID from 'tests/config.ini'
            self.assertEqual(
                megadebrid.config.get_ajax_info()["USER-AGENT"],
                "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            )
            self.assertEqual(
                megadebrid.config.get_ajax_info()["COOKIES"],
                {
                    "PHPSESSID": "CCCCCCCCCCCCCCCCCCCCCCCCCC",
                    "11111111111111111111111111111111": "1234567890123456",
                    "22222222222222222222222222222222": "12345678901234567890123456789012345678901234",
                },
            )
            # Read API Token from 'tests/config.ini'
            self.assertEqual(
                megadebrid.config.get_api_token(), "XXXXXXXXXXXXXXXXXXXXXXXXXX"
            )

    @patch("builtins.open", mock_open(read_data=""))
    # @patch.dict(environ, {"MEGA_USER": "user", "MEGA_PASSWD": "password"})
    async def test_env_var_credentials(self):
        """
        Test read CREDENTIALS from environment variable
        """

        with patch.dict(
            environ, {"MEGA_USER": "user", "MEGA_PASSWD": "password"}, clear=True
        ):
            async with MegaDebrid() as megadebrid:
                self.assertEqual(
                    megadebrid.config.get_credentials(),
                    {"Username": "user", "Password": "password"},
                )

    @patch("builtins.open", mock_open(read_data=""))
    # @patch.dict(environ, {"MEGA_TOKEN": "XXXXXXXXXXXXXXXXXXXXXXXXXX"})
    async def test_env_var_api(self):
        """
        Test read API token from environment variable
        """

        with patch.dict(
            environ, {"MEGA_TOKEN": "XXXXXXXXXXXXXXXXXXXXXXXXXX"}, clear=True
        ):
            async with MegaDebrid() as megadebrid:
                self.assertEqual(
                    megadebrid.config.get_api_token(), "XXXXXXXXXXXXXXXXXXXXXXXXXX"
                )

    @patch("builtins.open", mock_open(read_data=""))
    # @patch.dict(environ, {"MEGA_COOKIES": "{'PHPSESSID':'CCCCCCCCCCCCCCCCCCCCCCCCCC'}"})
    async def test_env_var_cookies(self):
        """
        Test read COOKIES from environment variable
        """

        with patch.dict(
            environ,
            {
                "MEGA_USER_AGENT": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                "MEGA_COOKIES": '{"PHPSESSID":"CCCCCCCCCCCCCCCCCCCCCCCCCC"}',
            },
            clear=True,
        ):
            async with MegaDebrid() as megadebrid:
                self.assertEqual(
                    megadebrid.config.get_ajax_info()["USER-AGENT"],
                    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                )
                self.assertEqual(
                    megadebrid.config.get_ajax_info()["COOKIES"],
                    {"PHPSESSID": "CCCCCCCCCCCCCCCCCCCCCCCCCC"},
                )

    async def test_hash_password(self):
        """
        Test hashing password as MD5 or return empty value
        """
        async with MegaDebrid() as megadebrid:
            self.assertEqual(megadebrid.hash_passwd(None), "")
            self.assertEqual(
                megadebrid.hash_passwd("test123"), "cc03e747a6afbbcbf8be7668acfebee5"
            )
