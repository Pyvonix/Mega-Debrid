from unittest import TestCase  # , IsolatedAsyncioTestCase
from unittest.mock import patch, mock_open

from megadebrid.worker.tasks import (
    save_file,
    debrid_and_save_file,
    download_magnet,
    download_torrent,
)


@patch(
    "builtins.open",
    mock_open(read_data=open("tests/config.ini", "r", encoding="utf-8").read()),
)
class TestMegaWorker(TestCase):
    """
    Test MegaWorker: celery tasks (not really useful)
    """

    @patch(
        "megadebrid.worker.tasks.save_file.delay",
        return_value="/tmp/file_example_PNG_1MB.png",
    )
    def test_task_save_file(self, mocked_task_save_file):
        """
        Test to reach the task function save_file before being sent to worker
        """
        url = "https://file-examples.com/storage/feeb72b10363daaeba4c0c9/2017/10/file_example_PNG_1MB.png"

        created_task = save_file.delay(url, "/tmp")
        self.assertIsNotNone(created_task)

        self.assertEqual(mocked_task_save_file.call_count, 1)
        self.assertEqual(mocked_task_save_file.call_args.args, (url, "/tmp"))

    @patch("megadebrid.worker.tasks.debrid_and_save_file.delay")
    def test_debrid_and_save_file(self, mocked_task_debrid_and_save_file):
        """
        Test to reach the task function debrid_and_save_file before being sent to worker
        """
        link = "https://1fichier.com/?xxxxxxxxxxxx"

        created_task = debrid_and_save_file.delay(link, "/tmp")
        self.assertIsNotNone(created_task)

        self.assertEqual(mocked_task_debrid_and_save_file.call_count, 1)
        self.assertEqual(
            mocked_task_debrid_and_save_file.call_args.args, (link, "/tmp")
        )

    @patch("megadebrid.worker.tasks.download_magnet.delay")
    def test_download_magnet(self, mocked_task_download_magnet):
        """
        Test to reach the task function download_magnet before being sent to worker
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

        created_task = download_magnet.delay(magnet, "/tmp")
        self.assertIsNotNone(created_task)

        self.assertEqual(mocked_task_download_magnet.call_count, 1)
        self.assertEqual(mocked_task_download_magnet.call_args.args, (magnet, "/tmp"))

    @patch("megadebrid.worker.tasks.download_torrent.delay")
    def test_download_torrent(self, mocked_task_download_torrent):
        """
        Test to reach the task function download_torrent before being sent to worker
        """
        torrent_path = "/tmp/file.torrent"

        created_task = download_torrent.delay(torrent_path, "/tmp")
        self.assertIsNotNone(created_task)

        self.assertEqual(mocked_task_download_torrent.call_count, 1)
        self.assertEqual(
            mocked_task_download_torrent.call_args.args, (torrent_path, "/tmp")
        )
