import asyncio
from bs4 import BeautifulSoup

from megadebrid.libs.base import MegaDebrid


class MegaDebridAjax(MegaDebrid):
    """
    Mega-Debrid AJAX: provide the methods to perform similar actions than AJAX backend.
    """

    def __init__(self) -> MegaDebrid:
        super().__init__(is_ajax=True)
        self.is_authenticated()

    @property
    def ajax_url(self) -> str:
        return f"{ self.base_url }/"

    def is_authenticated(self):
        if not self.session.headers.get("USER-AGENT"):
            raise Exception(
                "Require the same USER-AGENT that was used for authentication."
            )

        cookies = {cookie.key: cookie.value for cookie in self.session.cookie_jar}

        if not cookies.get("PHPSESSID"):
            raise Exception(
                "Could not authenticate on Mega-Debrid.eu: require to have PHPSESSID define."
            )

    async def get_torrents_list(self) -> dict:
        """
        GET the JSON list of my torrents in the seedbox
        on https://www.mega-debrid.eu/index.php?page=torrents
        """
        params = {"ajax": "getMyTorrents"}

        async with self.session.get(self.base_url, params=params) as response:
            return await response.json(content_type="text/html")

    async def get_torrent_status(self, torrent_id: str) -> dict:
        """
        POST torrent(s) id(s) to have the current status of the elements wished to be uploaded on the seedbox
        on https://www.mega-debrid.eu/index.php?ajax=statusTorrent
        """
        params = {"ajax": "statusTorrent"}
        data = {"torrentId[]": torrent_id}

        async with self.session.post(
            self.base_url, params=params, data=data
        ) as response:
            return await response.json(content_type="text/html")

    async def upload_magnet(self, magnet: str) -> dict:
        """
        POST a magnet link on the seedbox to be processed
        on https://www.mega-debrid.eu/index.php?ajax=uploadMagnet
        """
        params = {"ajax": "uploadMagnet"}
        data = {
            "magnet": magnet,
            "splitSizeFile": "0",
        }

        async with self.session.post(
            self.base_url, params=params, data=data
        ) as response:
            return await response.json(content_type="text/html")

    async def upload_torrent(self, torrent: str, split_size_file: int = 0) -> dict:
        """
        POST torrent file on the seedbox to be processed
        on https://www.mega-debrid.eu/index.php?ajax=uploadTorrent
        """
        params = {"ajax": "uploadTorrent"}
        data = {
            "splitSizeFile": split_size_file,
            "torrent": open(torrent, "rb"),
        }

        async with self.session.post(
            self.base_url, params=params, data=data
        ) as response:
            return await response.json(content_type="text/html")

    async def remove_torrent(self, torrent_id: str) -> dict:
        """
        POST torrent id to remove torrent from the list of the seedbox
        on https://www.mega-debrid.eu/index.php?ajax=removeTorrent
        """
        params = {"ajax": "removeTorrent"}
        data = {"id": torrent_id}

        async with self.session.post(
            self.base_url, params=params, data=data
        ) as response:
            return await response.json(content_type="text/html")

    async def debrid_link(self, link: str, password: str = "") -> dict:
        """
        POST a link to be debrided
        on https://www.mega-debrid.eu/index.php?ajax=statusTorrent
        Content-Type: 'application/x-www-form-urlencoded'
        """
        params = {
            "ajax": "xhr_debrid",
            "onlyLinks": "false",
        }
        data = {
            "link": link,
            "i": "0",
            "password": password,
        }

        async with self.session.post(
            self.base_url, params=params, data=data
        ) as response:
            html_body = await response.text()

        soup = BeautifulSoup(html_body, "html.parser")
        debrid_code = soup.find(id="debrid_0")["data-code"]

        params = {
            "ajax": "debrid",
            "json": "1",
        }
        data = {"code": debrid_code}

        async with self.session.post(
            self.base_url, params=params, data=data
        ) as response:
            return await response.json(content_type="text/html")
