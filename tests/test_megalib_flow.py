from asynctempfile import NamedTemporaryFile
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, mock_open, AsyncMock
from aioresponses import aioresponses
from random import randbytes, randint
from pathlib import Path

from megadebrid.libs.flow import MegaDebridFlow


@patch(
    "builtins.open",
    mock_open(read_data=open("tests/config.ini", "r", encoding="utf-8").read()),
)
@patch("asyncio.sleep", AsyncMock())
class TestMegaDebridFlow(IsolatedAsyncioTestCase):
    """
    Test all async methods of MegaDebridFlow library
    """

    def setUp(self):
        super().setUp()
        self.nb = randint(1, 9)
        self.magnet = (
            "magnet:?xt=urn:btih:fb72d751bcc437746583c298ce395b84f3089e8f"
            "&dn=Rick.and.Morty.S06E01.WEBRip.mp4"
            "&tr=http%3A%2F%2Fexample.tracker.wf%3A7777%2Fannounce"
            "&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce"
            "&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce"
            "&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce"
            "&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce"
        )

    async def test_get_magnet_hash(self):
        """Test to get magnet hash in the magnet link"""

        async with MegaDebridFlow() as megadebrid:
            hash = megadebrid.get_magnet_hash(self.magnet)

        self.assertEqual(hash, "fb72d751bcc437746583c298ce395b84f3089e8f")

    @aioresponses()
    @patch("builtins.print")
    async def test_wait_until_complete(self, mocked, mocked_print):
        """
        Test to wait until the torrent status isn't complet on Mega-Debrid API
        """

        for i in range(0, 11):
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
                        "status": "in progress" if i != 10 else "complete",
                        "progress": f"{ 10 * i }",
                        "speed": f"{ randint(0,9) }.{ randint(10,99) }",
                        "peers": None,
                        "ub_link": None
                        if i != 10
                        else "https://1fichier.com/?xxxxxxxxxxxx",
                    },
                },
            )

        async with MegaDebridFlow() as megadebrid:
            response = await megadebrid.wait_until_complete(
                "fb72d751bcc437746583c298ce395b84f3089e8f"
            )

        self.assertEqual(response["response_code"], "ok")
        self.assertEqual(response["status"]["status"], "complete")
        self.assertIsNotNone(response["status"]["ub_link"])

    @aioresponses()
    @patch("megadebrid.libs.flow.aiopen", return_value=NamedTemporaryFile())
    async def test_save_file(self, mocked, mocked_aiopen):
        """
        Test to save a file with full asynchronous way (not specific to Mega-Debrid)
        """
        url = "https://file-examples.com/storage/feeb72b10363daaeba4c0c9/2017/10/file_example_PNG_1MB.png"
        saved_path = Path("/tmp/downloads/file_example_PNG_1MB.png")

        mocked.add(
            method="GET",
            status=200,
            url="https://file-examples.com/storage/feeb72b10363daaeba4c0c9/2017/10/file_example_PNG_1MB.png",
            content_type="image/png",
            body=b"\x89\x50\x4e\x47" + randbytes(1024 * 1024),
        )

        async with MegaDebridFlow() as megadebrid:
            response = await megadebrid.save_file(url, "/tmp/downloads/")

        self.assertIsInstance(response, Path)
        self.assertEqual(response, saved_path)

    @aioresponses()
    @patch("megadebrid.libs.flow.aiopen", return_value=NamedTemporaryFile())
    async def test_debrid_and_save_file(self, mocked, mocked_aiopen):
        """
        Test to unrestrict a link and save the file at generated based on async save_file on Mega-Debrid API
        """
        link = "https://1fichier.com/?xxxxxxxxxxxx"  # ? could be links
        saved_path = Path("/tmp/downloads/Rick.and.Morty.S06E01.WEBRip.mp4")

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
        mocked.add(
            method="GET",
            status=200,
            url=f"https://www{ self.nb }.unrestrict.link/download/file/xxxxxxxxxxxxxxx/Rick.and.Morty.S06E01.WEBRip.mp4",
            content_type="application/force-download",
            headers={
                "Content-Length": str(1024 * 1024 * 10),
                "Content-Disposition": 'attachment; filename="Rick.and.Morty.S06E01.WEBRip.mp4"',
                "Content-Transfer-Encoding": "binary",
            },
            body=randbytes(1024 * 1024 * 10),
        )

        async with MegaDebridFlow() as megadebrid:
            response = await megadebrid.debrid_and_save_file(link, "/tmp/downloads")

        self.assertIsInstance(response, Path)
        self.assertEqual(response, saved_path)

    @aioresponses()
    @patch("builtins.print")
    @patch("megadebrid.libs.flow.aiopen", return_value=NamedTemporaryFile())
    async def test_download_magnet(self, mocked, mocked_aiopen, mocked_print):
        """
        Test to 'add a magnet link' on the Torrent Converter, wait until the torrent have been uploaded
        on 1fichier then unrestrict it and finally download it. Everything through Mega-Debrid API
        """
        saved_path = Path("/tmp/downloads/Rick.and.Morty.S06E01.WEBRip.mp4")

        # Torrent Converter: Submission of the magnet link
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
        # Torrent Converter: Starting
        mocked.add(
            method="POST",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=getTorrent&token=XXXXXXXXXXXXXXXXXXXXXXXXXX",
            content_type="text/html; charset=UTF-8",
            payload={
                "response_code": "ok",
                "status": {
                    "name": "Rick.and.Morty.S06E01.WEBRip",
                    "nbFiles": "0",
                    "size": "0",
                    "status": "pending",
                    "progress": "0",
                    "speed": "0.00",
                    "peers": "0",
                    "ub_link": None,
                },
            },
        )
        # Torrent Converter: Pending/Downloading
        for i in range(0, 11):
            mocked.add(
                method="POST",
                status=200,
                url="https://www.mega-debrid.eu/api.php?action=getTorrent&token=XXXXXXXXXXXXXXXXXXXXXXXXXX",
                content_type="text/html; charset=UTF-8",
                payload={
                    "response_code": "ok",
                    "status": {
                        "name": "Rick.and.Morty.S06E01.WEBRip",
                        "nbFiles": "0",
                        "size": "576931826",
                        "status": "pending",
                        "progress": f"{ i * 10 }",
                        "speed": "0.00",
                        "peers": f"{ randint(0, 20) }",
                        "ub_link": None,
                    },
                },
            )
        # Torrent Converter: Downloaded
        mocked.add(
            method="POST",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=getTorrent&token=XXXXXXXXXXXXXXXXXXXXXXXXXX",
            content_type="text/html; charset=UTF-8",
            payload={
                "response_code": "ok",
                "status": {
                    "name": "Rick.and.Morty.S06E01.WEBRip.mp4",
                    "nbFiles": "0",
                    "size": "576931826",
                    "status": "downloaded",
                    "progress": "100",
                    "speed": "0.00",
                    "peers": "19",
                    "ub_link": None,
                },
            },
        )
        # Torrent Converter: Queued
        mocked.add(
            method="POST",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=getTorrent&token=XXXXXXXXXXXXXXXXXXXXXXXXXX",
            content_type="text/html; charset=UTF-8",
            payload={
                "response_code": "ok",
                "status": {
                    "name": "Rick.and.Morty.S06E01.WEBRip.mp4",
                    "nbFiles": "0",
                    "size": "576931826",
                    "status": "queued",
                    "progress": "100",
                    "speed": "0.00",
                    "peers": "19",
                    "ub_link": None,
                },
            },
        )
        # Torrent Converter: Complete
        mocked.add(
            method="POST",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=getTorrent&token=XXXXXXXXXXXXXXXXXXXXXXXXXX",
            content_type="text/html; charset=UTF-8",
            payload={
                "response_code": "ok",
                "status": {
                    "name": "Rick.and.Morty.S06E01.WEBRip.mp4",
                    "nbFiles": "0",
                    "size": "576931826",
                    "status": "complete",
                    "progress": "100",
                    "speed": "0.00",
                    "peers": "16",
                    "ub_link": "https://1fichier.com/?xxxxxxxxxxxx",
                },
            },
        )
        # Download: Unrestrict link
        mocked.add(
            method="POST",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=getLink&token=XXXXXXXXXXXXXXXXXXXXXXXXXX",
            content_type="text/html; charset=UTF-8",
            # aioresponses doesn't support matchers like responses: https://github.com/pnuckowski/aioresponses/issues/213
            # match=[
            #    matchers.json_params_matcher({'link': 'https://1fichier.com/?xxxxxxxxxxxx', 'password': None)
            # ],
            payload={
                "response_code": "ok",
                "response_text": "",
                "debridLink": f"https://www{ self.nb }.unrestrict.link/download/file/xxxxxxxxxxxxxxx/Rick.and.Morty.S06E01.WEBRip.mp4",
                "filename": "Rick.and.Morty.S06E01.WEBRip.mp4",
            },
        )
        # Download: Saving unrestricted file
        mocked.add(
            method="GET",
            status=200,
            url=f"https://www{ self.nb }.unrestrict.link/download/file/xxxxxxxxxxxxxxx/Rick.and.Morty.S06E01.WEBRip.mp4",
            content_type="application/force-download",
            headers={
                "Content-Length": str(1024 * 1024 * 10),
                "Content-Disposition": 'attachment; filename="Rick.and.Morty.S06E01.WEBRip.mp4"',
                "Content-Transfer-Encoding": "binary",
            },
            body=randbytes(1024 * 1024 * 10),
        )

        async with MegaDebridFlow() as megadebrid:
            response = await megadebrid.download_magnet(self.magnet, "/tmp/downloads")

        self.assertIsInstance(response, Path)
        self.assertEqual(response, saved_path)

    @aioresponses()
    @patch("megadebrid.libs.flow.aiopen", return_value=NamedTemporaryFile())
    async def test_download_magnet_duplicate(self, mocked, mocked_aiopen):
        """
        Test connect user on Mega-Debrid API with wrong credentials
        """
        # saved_path = Path("/tmp/downloads/Rick.and.Morty.S06E01.WEBRip.mp4")

        # Torrent Converter: Submission magnet link that already exists
        mocked.add(
            method="POST",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=uploadTorrent&token=XXXXXXXXXXXXXXXXXXXXXXXXXX",
            content_type="text/html; charset=UTF-8",
            payload={"response_code": "nok", "response_text": "Torrent duplicate"},
            repeat=True,
        )

        # async with MegaDebridFlow() as megadebrid:
        #    response = await megadebrid.download_magnet(self.magnet, '/tmp/downloads')

        # self.assertIsInstance(response, Path)
        # self.assertEqual(response, saved_path)
        pass

    @aioresponses()
    @patch("builtins.print")
    @patch("builtins.open", new_callable=mock_open, read_data=randbytes(1024 * 10))
    @patch("megadebrid.libs.flow.aiopen", return_value=NamedTemporaryFile())
    async def test_download_torrent(
        self, mocked, mocked_aiopen, mocked_open, mocked_print
    ):
        """
        Test to 'add a torrent' on the Torrent Converter, wait until the torrent have been uploaded
        on 1fichier then unrestrict it and finally download it. Everything through Mega-Debrid API
        """
        torrent_path = Path("/tmp/Rick.and.Morty.S06E01.WEBRip.mp4.torrent")
        saved_path = Path("/tmp/downloads/Rick.and.Morty.S06E01.WEBRip.mp4")

        # Torrent Converter: Submission of the torrent file
        # It's possible to POST multiple time the same torrent file, that will return the same response (no duplicate).
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
        # Torrent Converter: Starting
        mocked.add(
            method="POST",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=getTorrent&token=XXXXXXXXXXXXXXXXXXXXXXXXXX",
            content_type="text/html; charset=UTF-8",
            payload={
                "response_code": "ok",
                "status": {
                    "name": "Rick.and.Morty.S06E01.WEBRip",
                    "nbFiles": "0",
                    "size": "0",
                    "status": "pending",
                    "progress": "0",
                    "speed": "0.00",
                    "peers": "0",
                    "ub_link": None,
                },
            },
        )
        # Torrent Converter: Pending/Downloading
        for i in range(0, 11):
            mocked.add(
                method="POST",
                status=200,
                url="https://www.mega-debrid.eu/api.php?action=getTorrent&token=XXXXXXXXXXXXXXXXXXXXXXXXXX",
                content_type="text/html; charset=UTF-8",
                payload={
                    "response_code": "ok",
                    "status": {
                        "name": "Rick.and.Morty.S06E01.WEBRip",
                        "nbFiles": "0",
                        "size": "576931826",
                        "status": "pending",
                        "progress": f"{ i * 10 }",
                        "speed": "0.00",
                        "peers": f"{ randint(0, 20) }",
                        "ub_link": None,
                    },
                },
            )
        # Torrent Converter: Downloaded
        mocked.add(
            method="POST",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=getTorrent&token=XXXXXXXXXXXXXXXXXXXXXXXXXX",
            content_type="text/html; charset=UTF-8",
            payload={
                "response_code": "ok",
                "status": {
                    "name": "Rick.and.Morty.S06E01.WEBRip.mp4",
                    "nbFiles": "0",
                    "size": "576931826",
                    "status": "downloaded",
                    "progress": "100",
                    "speed": "0.00",
                    "peers": "19",
                    "ub_link": None,
                },
            },
        )
        # Torrent Converter: Queued
        mocked.add(
            method="POST",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=getTorrent&token=XXXXXXXXXXXXXXXXXXXXXXXXXX",
            content_type="text/html; charset=UTF-8",
            payload={
                "response_code": "ok",
                "status": {
                    "name": "Rick.and.Morty.S06E01.WEBRip.mp4",
                    "nbFiles": "0",
                    "size": "576931826",
                    "status": "queued",
                    "progress": "100",
                    "speed": "0.00",
                    "peers": "19",
                    "ub_link": None,
                },
            },
        )
        # Torrent Converter: Complete
        mocked.add(
            method="POST",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=getTorrent&token=XXXXXXXXXXXXXXXXXXXXXXXXXX",
            content_type="text/html; charset=UTF-8",
            payload={
                "response_code": "ok",
                "status": {
                    "name": "Rick.and.Morty.S06E01.WEBRip.mp4",
                    "nbFiles": "0",
                    "size": "576931826",
                    "status": "complete",
                    "progress": "100",
                    "speed": "0.00",
                    "peers": "16",
                    "ub_link": "https://1fichier.com/?xxxxxxxxxxxx",
                },
            },
        )
        # Download: Unrestrict link
        mocked.add(
            method="POST",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=getLink&token=XXXXXXXXXXXXXXXXXXXXXXXXXX",
            content_type="text/html; charset=UTF-8",
            # aioresponses doesn't support matchers like responses: https://github.com/pnuckowski/aioresponses/issues/213
            # match=[
            #    matchers.json_params_matcher({'link': 'https://1fichier.com/?xxxxxxxxxxxx', 'password': None)
            # ],
            payload={
                "response_code": "ok",
                "response_text": "",
                "debridLink": f"https://www{ self.nb }.unrestrict.link/download/file/xxxxxxxxxxxxxxx/Rick.and.Morty.S06E01.WEBRip.mp4",
                "filename": "Rick.and.Morty.S06E01.WEBRip.mp4",
            },
        )
        # Download: Saving unrestricted file
        mocked.add(
            method="GET",
            status=200,
            url=f"https://www{ self.nb }.unrestrict.link/download/file/xxxxxxxxxxxxxxx/Rick.and.Morty.S06E01.WEBRip.mp4",
            content_type="application/force-download",
            headers={
                "Content-Length": str(1024 * 1024 * 10),
                "Content-Disposition": 'attachment; filename="Rick.and.Morty.S06E01.WEBRip.mp4"',
                "Content-Transfer-Encoding": "binary",
            },
            body=randbytes(1024 * 1024 * 10),
        )

        async with MegaDebridFlow() as megadebrid:
            response = await megadebrid.download_torrent(torrent_path, "/tmp/downloads")

        self.assertIsInstance(response, Path)
        self.assertEqual(response, saved_path)
