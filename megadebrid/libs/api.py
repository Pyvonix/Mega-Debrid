import asyncio
from typing import Optional, Any

from megadebrid.libs.base import MegaDebrid
from megadebrid.utils.decorators import renew_obsolete_token


class MegaDebridApi(MegaDebrid):
    """
    Mega-Debrid API: provide the methods to perform the authorized actions through API backend.
    Source: https://www.mega-debrid.eu/index.php?page=api
    WARNING : If you send more than 50 requests per seconds, your IP address will be banned for 1 day.
    """

    def __init__(self) -> None:
        super().__init__()
        self.api_token = self.config.get_api_token()

    @property
    def api_url(self) -> str:
        return f"{ self.base_url }/api.php"

    async def __aenter__(self):
        await super().__aenter__()
        await self.get_token()
        return self

    async def get_token(self, is_renew: bool = False) -> None:
        """Verify if token is present config, else authenticate user with his credentials"""
        if not self.api_token:
            response = await self.connect_user()
            self.api_token = response.get("token")

            if not self.api_token:
                # and not is_renew:
                raise Exception(
                    "Could not authenticate on Mega-Debrid API: require to have token."
                )

            # Save token
            if False:
                self.config.save_api_token(self.api_token)

    async def connect_user(self) -> dict[str, str]:
        """
        Connect user:
        URL: https://www.mega-debrid.eu/api.php?action=connectUser&login=[user_login]&password=[user_password]
        WARNING : After 4 login failed (bad login/password), your IP address will be banned for some minutes.
        """
        credentials = self.config.get_credentials()

        params = {
            "action": "connectUser",
            "login": credentials["Username"],
            "password": credentials["Password"],
        }

        async with self.session.get(self.api_url, params=params) as response:
            return await response.json(content_type="text/html")

    @renew_obsolete_token
    async def get_user_history(self) -> dict[str, Any]:
        """
        Get user history:
        URL: https://www.mega-debrid.eu/api.php?action=getUserHistory&token=[token]
        """

        params = {
            "action": "getUserHistory",
            "token": self.api_token,
        }

        async with self.session.get(self.api_url, params=params) as response:
            return await response.json(content_type="text/html")

    @renew_obsolete_token
    async def get_hosters_list(self) -> dict[str, Any]:
        """
        Get hosters list:
        URL: https://www.mega-debrid.eu/api.php?action=getHostersList
        """
        params = {"action": "getHostersList"}

        async with self.session.get(self.api_url, params=params) as response:
            return await response.json(content_type="text/html")

    @renew_obsolete_token
    async def upload_magnet(self, magnet: str) -> dict[str, Any]:
        """
        Upload torrent (magnet URL of the torrent):
        URL: https://www.mega-debrid.eu/api.php?action=uploadTorrent&token=[token]
        """
        params = {
            "action": "uploadTorrent",
            "token": self.api_token,
        }

        async with self.session.post(
            self.api_url, params=params, data={"magnet": magnet}
        ) as response:
            return await response.json(content_type="text/html")

    @renew_obsolete_token
    async def upload_torrent(self, torrent: str) -> dict[str, Any]:
        """
        Upload torrent (upload file directly):
        URL: https://www.mega-debrid.eu/api.php?action=uploadTorrent&token=[token]
        """
        params = {
            "action": "uploadTorrent",
            "token": self.api_token,
        }

        async with self.session.post(
            self.api_url, params=params, data={"file": open(torrent, "rb")}
        ) as response:
            return await response.json(content_type="text/html")

    @renew_obsolete_token
    async def get_torrents_list(self) -> dict[str, Any]:
        """
        Get Torrents list:
        URL: https://www.mega-debrid.eu/api.php?action=getTorrents&token=[token]
        """
        params = {
            "action": "getTorrents",
            "token": self.api_token,
        }

        async with self.session.get(self.api_url, params=params) as response:
            return await response.json(content_type="text/html")

    @renew_obsolete_token
    async def get_torrent_status(self, torrent_hash: str) -> dict[str, Any]:
        """
        Get torrent information:
        URL: https://www.mega-debrid.eu/api.php?action=getTorrent&token=[token]
        """
        params = {
            "action": "getTorrent",
            "token": self.api_token,
        }

        async with self.session.post(
            self.api_url, params=params, data={"hash": torrent_hash}
        ) as response:
            return await response.json(content_type="text/html")

    @renew_obsolete_token
    async def debrid_link(
        self, link: str, password: Optional[str] = None
    ) -> dict[str, str]:
        """
        Get debrid link:
        URL: https://www.mega-debrid.eu/api.php?action=getLink&token=[token]
        """
        params = {
            "action": "getLink",
            "token": self.api_token,
        }
        data = {
            "link": link,
            "password": self.hash_passwd(password),
        }

        async with self.session.post(
            self.api_url, params=params, data=data
        ) as response:
            return await response.json(content_type="text/html")
