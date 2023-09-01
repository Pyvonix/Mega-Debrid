from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, mock_open
from aioresponses import aioresponses
from random import randbytes, randint
from pathlib import Path

from megadebrid.libs.ajax import MegaDebridAjax


@patch(
    "builtins.open",
    mock_open(read_data=open("tests/config.ini", "r", encoding="utf-8").read()),
)
class TestMegaDebridAjax(IsolatedAsyncioTestCase):
    """
    Test all async methods of MegaDebridAjax library
    """

    def setUp(self):
        super().setUp()
        self.nb = randint(1, 9)

    @aioresponses()
    async def test_get_torrents_list(self, mocked):
        """
        Test to get the list of torrents from Mega-Debrid account
        """
        mocked.add(
            method="GET",
            status=200,
            url="https://www.mega-debrid.eu/?ajax=getMyTorrents",
            content_type="text/html; charset=UTF-8",
            payload={
                "response_code": "ok",
                "torrents": [
                    {
                        "id": "55117",
                        "hash": "78bb835326b3fd39f2d1c27d0986b25ae50eeb07",
                        "transmission_id": "45",
                        "name": "Rick.and.Morty.S06E01.WEBRip.mp4",
                        "nbFiles": "0",
                        "upload_url": "",
                        "size": "20492695023",
                        "status": "complete",
                        "error": "",
                        "progress": "100",
                        "speed": "0.00",
                        "peers": None,
                        "ub_link": "https://1fichier.com/?AAAAAAAAAAAAAAAAAAAA",
                        "idCompte": "1",
                        "ipMembre": "127.0.0.1",
                        "date": "2022-01-01 12:00:00",
                        "serveur_id": "0",
                        "split_file_size": "0",
                        "magnet_hash": None,
                    },
                    {
                        "id": "58545",
                        "hash": "06cb0d45eba9e7346aa15fed70e98bcc749e632b",
                        "transmission_id": "45",
                        "name": "Rick.and.Morty.S06E02.WEBRip.mp4",
                        "nbFiles": "0",
                        "upload_url": "",
                        "size": "20482675043",
                        "status": "in progress",
                        "error": "",
                        "progress": "42",
                        "speed": "25.00",
                        "peers": None,
                        "ub_link": "https://1fichier.com/?BBBBBBBBBBBBBBBBBBBB",
                        "idCompte": "1",
                        "ipMembre": "127.0.0.1",
                        "date": "2022-01-01 14:00:00",
                        "serveur_id": "0",
                        "split_file_size": "0",
                        "magnet_hash": None,
                    },
                ],
            },
        )

        async with MegaDebridAjax() as megadebrid:
            response = await megadebrid.get_torrents_list()

        self.assertEqual(response["response_code"], "ok")
        self.assertIsInstance(response["torrents"], list)
        self.assertEqual(len(response["torrents"]), 2)

    @aioresponses()
    async def test_get_torrent_status(self, mocked):
        """
        Test to get the current status of a torrent(s) processed on Mega-Debrid account
        """
        torrent_id = "58545"

        mocked.add(
            method="POST",
            url="https://www.mega-debrid.eu/?ajax=statusTorrent",
            status=200,
            content_type="text/html; charset=UTF-8",
            payload={
                "response_code": "ok",
                "torrents": {
                    torrent_id: {
                        "state": "downloading",
                        "progress": 12.6199999999999999,
                        "speed": 1.56,
                        "peers": 53,
                        "eta": 885,
                        "name": "New torrent",
                        "size": 1471893268,
                    }
                },
            },
        )

        async with MegaDebridAjax() as megadebrid:
            response = await megadebrid.get_torrent_status(torrent_id)

        self.assertEqual(response["response_code"], "ok")
        self.assertIsInstance(response["torrents"], dict)
        self.assertEqual(list(response["torrents"].keys())[0], torrent_id)
        # test torrents_id = ['XXXX', 'XXXX']

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
            url="https://www.mega-debrid.eu/?ajax=uploadMagnet",
            status=200,
            content_type="text/html; charset=UTF-8",
            payload={
                "response_code": "ok",
                "name": "Rick.and.Morty.S06E01.WEBRip.mp4",
                "size": None,
                "id": 122,  # this 'id' will be the 'transmission_id' on my torrents list
            },
        )
        mocked.add(
            method="POST",
            url="https://www.mega-debrid.eu/?ajax=uploadMagnet",
            status=200,
            content_type="text/html; charset=UTF-8",
            payload={"response_code": "nok", "error": "Torrent duplicate"},
            repeat=True,  # Any other POST request with the same magnet will result to 'Torrent duplicate'
        )

        async with MegaDebridAjax() as megadebrid:
            response = await megadebrid.upload_magnet(magnet)

            self.assertEqual(response["response_code"], "ok")
            self.assertEqual(response["name"], "Rick.and.Morty.S06E01.WEBRip.mp4")

            response = await megadebrid.upload_magnet(magnet)

            self.assertEqual(response["response_code"], "nok")
            self.assertEqual(response["error"], "Torrent duplicate")

    @aioresponses()
    @patch("builtins.open", new_callable=mock_open, read_data=randbytes(1024 * 10))
    async def test_upload_torrent(self, mocked, mocked_open):
        """
        Test to upload a torrent file on Mega-Debrid account
        """
        torrent_path = Path("/tmp/Rick.and.Morty.S06E01.WEBRip.mp4.torrent")

        # It's possible to POST multiples time the same torrent, it will return the same response and
        # add it multiples time to the torrents list
        mocked.add(
            method="POST",
            url="https://www.mega-debrid.eu/?ajax=uploadTorrent",
            status=200,
            content_type="text/html; charset=UTF-8",
            payload={
                "response_code": "ok",
                "name": "Rick.and.Morty.S06E01.WEBRip.mp4",
                "size": 0,
                "id": 122,
            },  # this 'id' will be the 'transmission_id' on my torrents list
            repeat=True,
        )

        async with MegaDebridAjax() as megadebrid:
            response = await megadebrid.upload_torrent(torrent_path)

        self.assertEqual(response["response_code"], "ok")
        self.assertEqual(response["name"], torrent_path.name[: -len(".torrent")])

    @aioresponses()
    async def test_remove_torrent(self, mocked):
        """
        Test to remove a torrent from Mega-Debrid account
        """
        torrent_id = "44404"
        torrents_id = "44404,44406,44408"

        mocked.add(
            method="POST",
            url="https://www.mega-debrid.eu/?ajax=removeTorrent",
            status=200,
            content_type="text/html; charset=UTF-8",
            payload={"response_code": "ok"},
            repeat=True,  # Same response for one id and multiples id
        )

        async with MegaDebridAjax() as megadebrid:
            response = await megadebrid.remove_torrent(torrent_id)
            self.assertEqual(response["response_code"], "ok")

            response = await megadebrid.remove_torrent(torrents_id)
            self.assertEqual(response["response_code"], "ok")

    @aioresponses()
    async def test_debrid_link(self, mocked):
        """
        Test to debrik link(s) with it Mega-Debrid account
        """
        link = (
            "https://1fichier.com/?CCCCCCCCCCCCCCCCCCCC"  # ? Could be mutliplies links
        )

        mocked.add(
            method="POST",
            url="https://www.mega-debrid.eu/?ajax=xhr_debrid&onlyLinks=false",
            status=200,
            content_type="text/html; charset=UTF-8",
            body=f"\n"
            f"<div id='' class='acp-box col-md-6 card'><h3> <span class='title'>{ link }</span>"
            f"<span class='infos'><i class='fa fa-info-circle'></i> <span name='info-content'>ID: #6666<br> (Server used at 12.48%)</span>"
            f"</h3><span class='hoster'> <img src='/images/hosts/unfichier.png' title='Unfichier'></span>"
            f"<div class='card-body'><span class='filename'>My_File</span><span class='size'>1388 MB </span></div>"
            f"<div class='span-debrid'><span id='debrid_0' align='center' data-code='30561724716e3ec' data-i='0'>"
            f"<button class='btn btn-primary'><i class='fa fa-play'></i></button></span></div></div>",
        )
        mocked.add(
            method="POST",
            url="https://www.mega-debrid.eu/?ajax=debrid&json=1",
            status=200,
            content_type="text/html; charset=UTF-8",
            payload={
                "text": "Download my file",
                "link": f"https://www{ self.nb }.unrestrict.link/download/file/30561724716e3ec/My_File.mkv",
                "video": "http://www.mega-debrid.eu/index.php?page=streaming&id=30561724716e3ec",
                "autoDl": True,
            },
        )

        async with MegaDebridAjax() as megadebrid:
            response = await megadebrid.debrid_link(link)

        self.assertIn("unrestrict.link/download/file/", response["link"])
        self.assertIn(
            "http://www.mega-debrid.eu/index.php?page=streaming&id=", response["video"]
        )
