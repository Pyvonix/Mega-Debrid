import asyncio
from hashlib import md5
from aiohttp import ClientSession

from megadebrid.parsers.configparser import MegaConfigParser


class MegaDebrid:
    DOMAIN = "www.mega-debrid.eu"

    def __init__(self, *args, **kwargs) -> None:
        self.config = MegaConfigParser(config_path=kwargs.pop("config", None))

        ajax_config = (
            self.config.get_ajax_info() if kwargs.pop("is_ajax", False) else {}
        )
        headers = self.set_headers(ajax_config["USER-AGENT"]) if ajax_config else {}
        cookies = ajax_config["COOKIES"] if ajax_config else {}

        self.session = ClientSession(headers=headers, cookies=cookies)

    async def __aenter__(self):
        # Called when enter in 'async with MegaDebrid() as megadebrid:'
        return self

    async def __aexit__(self, *err):
        # Called when leave 'async with MegaDebrid() as megadebrid:'
        await self.session.close()
        self.session = None

    @property
    def base_url(self) -> str:
        return f"https://{ self.DOMAIN }"

    def set_headers(self, user_agent) -> dict:
        """
        Return the required headers to make the request.
        Important: 'User-Agent' must be the same as the one that generated the cookies.
        """
        return {
            "User-Agent": user_agent,
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": "https://www.mega-debrid.eu/index.php",
            "X-Requested-With": "XMLHttpRequest",
        }

    @staticmethod
    def hash_passwd(password):
        """Password is md5 encoded"""
        return md5(password.encode()).hexdigest() if password else ""
