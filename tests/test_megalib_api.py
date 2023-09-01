from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, mock_open
from aioresponses import aioresponses
from random import randbytes, randint
from pathlib import Path

from megadebrid.libs.api import MegaDebridApi


@patch(
    "builtins.open",
    mock_open(read_data=open("tests/config.ini", "r", encoding="utf-8").read()),
)
class TestMegaDebridApi(IsolatedAsyncioTestCase):
    """
    Test all async methods of MegaDebridApi library
    """

    def setUp(self):
        super().setUp()
        self.nb = randint(1, 9)

    @aioresponses()
    async def test_connect_user_failure(self, mocked):
        """
        Test connect user on Mega-Debrid API with wrong credentials
        """

        mocked.add(
            method="GET",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=connectUser&login=user&password=password",
            content_type="text/html; charset=UTF-8",
            payload={
                "response_code": "UNKNOWN_USER",
                "response_text": "User and password doesn't match",
                "retry": "1",
            },
        )

        async with MegaDebridApi() as megadebrid:
            response = await megadebrid.connect_user()

        self.assertEqual(response["response_code"], "UNKNOWN_USER")
        self.assertEqual(response["response_text"], "User and password doesn't match")

    @aioresponses()
    async def test_connect_user_succeeded(self, mocked):
        """
        Test connect user on Mega-Debrid API with correct credentials
        """

        mocked.add(
            method="GET",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=connectUser&login=user&password=password",
            content_type="text/html; charset=UTF-8",
            payload={
                "response_code": "ok",
                "response_text": "User logged",
                "token": "XXXXXXXXXXXXXXXXXXXXXXXXXX",
                "vip_end": "1111111111",
                "email": "user@example.com",
            },
        )

        async with MegaDebridApi() as megadebrid:
            response = await megadebrid.connect_user()

        self.assertEqual(response["response_code"], "ok")
        self.assertEqual(response["response_text"], "User logged")
        self.assertEqual(response["token"], "XXXXXXXXXXXXXXXXXXXXXXXXXX")

        # TODO: config upateded with token

    @aioresponses()
    async def test_get_user_history(self, mocked):
        """
        Test to get user history on Mega-Debrid API
        """

        mocked.add(
            method="GET",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=getUserHistory&token=XXXXXXXXXXXXXXXXXXXXXXXXXX",
            content_type="text/html; charset=UTF-8",
            payload={
                "response_code": "ok",
                "response_text": "",
                "history": [
                    {
                        "nom": "Rick.and.Morty.S06E01.WEBRip.mp4",
                        "heber": "uptobox",
                        "lien": "https://uptobox.com/xxxxxxxxxxxx",
                    },
                    {
                        "nom": "Rick.and.Morty.S06E02.WEBRip.mp4",
                        "heber": "uptobox",
                        "lien": "https://uptobox.com/xxxxxxxxxxxx",
                    },
                    {
                        "nom": "Rick.and.Morty.S06E03.WEBRip.mp4",
                        "heber": "unfichier",
                        "lien": "https://1fichier.com/?xxxxxxxxxxxx",
                    },
                    {
                        "nom": "Rick.and.Morty.S06E04.WEBRip.mp4",
                        "heber": "uptobox",
                        "lien": "https://uptobox.com/xxxxxxxxxxxx",
                    },
                    {
                        "nom": "Rick.and.Morty.S06E05.WEBRip.mp4",
                        "heber": "unfichier",
                        "lien": "https://1fichier.com/?xxxxxxxxxxxx",
                    },
                    {
                        "nom": "Rick.and.Morty.S06E06.WEBRip.mp4",
                        "heber": "uptobox",
                        "lien": "https://uptobox.com/wto5uq9iyf31",
                    },
                    {
                        "nom": "Rick.and.Morty.S06E07.WEBRip.mp4",
                        "heber": "rapidgator",
                        "lien": "https://rapidgator.net/file/xxxxxxxxxxxx",
                    },
                    {
                        "nom": "Rick.and.Morty.S06E08.WEBRip.mp4",
                        "heber": "unfichier",
                        "lien": "https://1fichier.com/?xxxxxxxxxxxx",
                    },
                    {
                        "nom": "Rick.and.Morty.S06E09.WEBRip.mp4",
                        "heber": "uptobox",
                        "lien": "https://uptobox.com/xxxxxxxxxxxx",
                    },
                    {
                        "nom": "Rick.and.Morty.S06E10.WEBRip.mp4",
                        "heber": "unfichier",
                        "lien": "https://1fichier.com/?xxxxxxxxxxxx",
                    },
                ],
            },
        )

        async with MegaDebridApi() as megadebrid:
            response = await megadebrid.get_user_history()

        self.assertEqual(response["response_code"], "ok")
        self.assertIsNotNone(response["history"])
        self.assertIsInstance(response["history"], list)

    @aioresponses()
    async def test_get_hosters_list(self, mocked):
        """
        Test to get Mega-Debrid hosters list on API
        """

        mocked.add(
            method="GET",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=getHostersList",
            content_type="text/html; charset=UTF-8",
            payload={
                "response_code": "ok",
                "response_text": "",
                "hosters": [
                    {
                        "name": "abcnews",
                        "url": "ABCNews",
                        "img": "https://cdn.mega-debrid.eu/images/hosts/abcnews.png",
                        "domains": ["abcnews.go.com"],
                        "status": "up",
                        "regexps": ["#http[s]*?://[www.]*?abcnews.go.com/.*?#msi"],
                        "type": "stream",
                    },
                    {
                        "name": "acast",
                        "url": "Acast",
                        "img": "https://cdn.mega-debrid.eu/images/hosts/acast.png",
                        "domains": ["acast.com"],
                        "status": "up",
                        "regexps": ["#http[s]*?://[www.]*?acast.com/.*?#msi"],
                        "type": "stream",
                    },
                    # And more...
                ],
            },
        )

        async with MegaDebridApi() as megadebrid:
            response = await megadebrid.get_hosters_list()

        self.assertEqual(response["response_code"], "ok")
        self.assertIsNotNone(response["hosters"])
        self.assertIsInstance(response["hosters"], list)

    @aioresponses()
    async def test_get_torrents_list(self, mocked):
        """
        Test to get the list of torrents on Mega-Debrid API
        """
        mocked.add(
            method="GET",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=getTorrents&token=XXXXXXXXXXXXXXXXXXXXXXXXXX",
            content_type="text/html; charset=UTF-8",
            payload={
                "response_code": "ok",
                "response_text": "",
                "torrents": [
                    {
                        "downloadLink": "https://1fichier.com/?AAAAAAAAAAAAAAAAAAAA",
                        "name": "Rick.and.Morty.S06E01.WEBRip.mp4",
                        "progress": "100",
                        "speed": "0.00",
                        "status": "complete",
                    },
                    {
                        "downloadLink": "https://1fichier.com/?BBBBBBBBBBBBBBBBBBBB",
                        "name": "Rick.and.Morty.S06E02.WEBRip.mp4",
                        "progress": "100",
                        "speed": "0.00",
                        "status": "complete",
                    },
                ],
            },
        )

        async with MegaDebridApi() as megadebrid:
            response = await megadebrid.get_torrents_list()

        self.assertEqual(response["response_code"], "ok")
        self.assertIsInstance(response["torrents"], list)
        self.assertEqual(len(response["torrents"]), 2)

    @aioresponses()
    async def test_get_torrent_status(self, mocked):
        """
        Test to get the torrent status on Mega-Debrid API
        """
        mocked.add(
            method="POST",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=getTorrent&token=XXXXXXXXXXXXXXXXXXXXXXXXXX",
            content_type="text/html; charset=UTF-8",
            payload={
                "response_code": "ok",
                "status": {
                    "name": "Rick.and.Morty.S06E01.WEBRip.mp4",
                    "nbFiles": "1",
                    "size": "576758736",
                    "status": "complete",
                    "progress": "100",
                    "speed": "0.00",
                    "peers": None,
                    "ub_link": "https://1fichier.com/?yelgngz7ta7j2i6j7db1",
                },
            },
        )

        async with MegaDebridApi() as megadebrid:
            response = await megadebrid.get_torrent_status(
                "fb72d751bcc437746583c298ce395b84f3089e8f"
            )

        self.assertEqual(response["response_code"], "ok")
        self.assertIsInstance(response["status"], dict)
        self.assertEqual(response["status"]["name"], "Rick.and.Morty.S06E01.WEBRip.mp4")
        self.assertEqual(response["status"]["status"], "complete")

    @aioresponses()
    async def test_upload_magnet(self, mocked):
        """
        Test to upload a magnet on Mega-Debrid account
        """
        magnet = (
            "magnet:?xt=urn:btih:fb72d751bcc437746583c298ce395b84f3089e8f"
            "&dn=Rick.and.Morty.S06E01.WEBRip.mp4"
            "&tr=http%3A%2F%2Fexample.tracker.wf%3A7777%2Fannounce"
            "&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce"
            "&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce"
            "&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce"
            "&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce"
        )

        mocked.add(
            method="POST",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=uploadTorrent&token=XXXXXXXXXXXXXXXXXXXXXXXXXX",
            content_type="text/html; charset=UTF-8",
            payload={
                "response_code": "ok",
                "response_text": "",
                "newTorrent": {
                    "hash": None,
                    "name": "Rick.and.Morty.S06E01.WEBRip.mp4",
                    "size": None,
                },
            },
        )
        # Any other POST request with the same magnet will result to 'Torrent duplicate'
        mocked.add(
            method="POST",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=uploadTorrent&token=XXXXXXXXXXXXXXXXXXXXXXXXXX",
            content_type="text/html; charset=UTF-8",
            payload={"response_code": "nok", "response_text": "Torrent duplicate"},
            repeat=True,
        )

        async with MegaDebridApi() as megadebrid:
            response = await megadebrid.upload_magnet(magnet)

            self.assertEqual(response["response_code"], "ok")
            self.assertIn("newTorrent", response)
            self.assertEqual(
                response["newTorrent"]["name"], "Rick.and.Morty.S06E01.WEBRip.mp4"
            )

            response = await megadebrid.upload_magnet(magnet)

            self.assertEqual(response["response_code"], "nok")
            self.assertEqual(response["response_text"], "Torrent duplicate")

    @aioresponses()
    @patch("builtins.open", new_callable=mock_open, read_data=randbytes(1024 * 10))
    async def test_upload_torrent(self, mocked, mocked_open):
        """
        Test to upload a torrent file on Mega-Debrid account
        """
        torrent_path = Path("/tmp/Rick.and.Morty.S06E01.WEBRip.mp4.torrent")

        # It's possible to POST multiple time the same torrent, that will return the same response.
        mocked.add(
            method="POST",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=uploadTorrent&token=XXXXXXXXXXXXXXXXXXXXXXXXXX",
            content_type="text/html; charset=UTF-8",
            payload={
                "response_code": "ok",
                "response_text": "",
                "newTorrent": {
                    "hash": "fb72d751bcc437746583c298ce395b84f3089e8f",
                    "name": "Rick.and.Morty.S06E01.WEBRip.mp4",
                    "size": 0,
                },
            },
            repeat=True,
        )

        async with MegaDebridApi() as megadebrid:
            response = await megadebrid.upload_torrent(torrent_path)

        self.assertEqual(response["response_code"], "ok")
        self.assertIn("newTorrent", response)
        self.assertEqual(
            response["newTorrent"]["name"], torrent_path.name[: -len(".torrent")]
        )

    @aioresponses()
    async def test_debrid_link(self, mocked):
        """
        Test to debrik link(s) with it Mega-Debrid account
        """
        link = "https://1fichier.com/?xxxxxxxxxxxx"  # ? could be links

        mocked.add(
            method="POST",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=getLink&token=XXXXXXXXXXXXXXXXXXXXXXXXXX",
            content_type="text/html; charset=UTF-8",
            payload={
                "response_code": "ok",
                "response_text": "",
                "debridLink": f"https://www{ self.nb }.unrestrict.link/download/file/xxxxxxxxxxxxxxx/Rick.and.Morty.S06E01.WEBRip.mp4",
                "filename": "Rick.and.Morty.S06E01.WEBRip.mp4",
            },
        )

        async with MegaDebridApi() as megadebrid:
            response = await megadebrid.debrid_link(link)

        self.assertEqual(response["response_code"], "ok")
        self.assertIn("unrestrict.link/download/file/", response["debridLink"])
