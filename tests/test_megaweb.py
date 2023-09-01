from unittest import TestCase  # , IsolatedAsyncioTestCase
from unittest.mock import patch, MagicMock

from uuid import UUID, uuid4

# import asyncio

from megadebrid.web import create_app
from megadebrid.web.views import TASKS_MAPPER


class TestMegaWeb(TestCase):
    """
    Test MegaWeb: Flask web interface/API correctly response and interact with celery tasks.
    Note: can't use IsolatedAsyncioTestCase due to test_client() doesn't support async
    """

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config.update(
            {
                "TESTING": True,
                "SERVER_NAME": "localhost",
                "WTF_CSRF_ENABLED": False,
                "PRESERVE_CONTEXT_ON_EXCEPTION": False,
            }
        )
        cls.client = cls.app.test_client()

    @staticmethod
    def is_valid_uuid(value: str):
        """
        Validate the provided value is a valid UUID
        """
        try:
            UUID(value)
            return True
        except ValueError:
            return False

    def test_megaweb_home(self):
        """
        Test home page is correctly render on browser
        """
        response = self.client.get("/")
        response_content = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "text/html; charset=utf-8")
        self.assertIn("<title>Mega-Web: Home</title>", response_content)
        # TODO: Add verification of forms

    def test_megaweb_create_unknown_task(self):
        """
        Test that a request without header 'Mega-Task' on the task creation endpoint return
        a response '400 Bad Request' containing related the error message.
        """
        response = self.client.post(
            "/tasks",
            json={"key": "value"},
            content_type="application/json",
            # No header specifying "Mega-Task" type
        )

        # Verify flask response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json["message"], "Bad Request")
        self.assertEqual(
            response.json["error"],
            f"You need specify a valid value for the header Mega-Task. "
            f"Allowed values are: { ', '.join(TASKS_MAPPER.keys()) }.",
        )

    def test_megaweb_create_task_wrong_args(self):
        """
        Test that a request without the correct argument on the task creation endpoint return
        a response '400 Bad Request' containing related the error message.
        """
        response = self.client.post(
            "/tasks",
            json={"key": "value"},
            content_type="application/json",
            headers={"Mega-Task": "SaveFile"},
        )

        # Verify flask response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json["message"], "Bad Request")
        self.assertIsNotNone(response.json["error"])

    @patch(
        "megadebrid.worker.tasks.save_file.delay", return_value=MagicMock(id=uuid4())
    )
    def test_megaweb_create_task_save_file(self, mocked_task_save_file):
        """
        Test that a request with header "Mega-Task: SaveFile" on Flask correctly reaches
        save_file function of MegaWorker (celery task).
        """
        url = "https://file-examples.com/storage/feeb72b10363daaeba4c0c9/2017/10/file_example_PNG_1MB.png"
        folder = "/tmp"

        response = self.client.post(
            "/tasks",
            json={"url": url, "folder": folder},
            content_type="application/json",
            headers={"Mega-Task": "SaveFile"},
        )

        # Verify celery task creation
        self.assertEqual(mocked_task_save_file.call_count, 1)
        self.assertEqual(
            mocked_task_save_file.call_args.kwargs, {"url": url, "folder": folder}
        )
        # Verify flask response
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(response.is_json)
        self.assertTrue(self.is_valid_uuid(response.json.get("task_id")))

    @patch(
        "megadebrid.worker.tasks.debrid_and_save_file.delay",
        return_value=MagicMock(id=uuid4()),
    )
    def test_megaweb_create_task_debrid_and_save_file(
        self, mocked_task_debrid_and_save_file
    ):
        """
        Test that a request with header "Mega-Task: DebridAndSaveFile" on Flask correctly reaches
        debrid_and_save_file function of MegaWorker (celery task).
        """
        link = "https://1fichier.com/?xxxxxxxxxxxx"
        folder = "/tmp"

        response = self.client.post(
            "/tasks",
            json={"link": link, "folder": folder},
            content_type="application/json",
            headers={"Mega-Task": "DebridAndSaveFile"},
        )

        # Verify celery task creation
        self.assertEqual(mocked_task_debrid_and_save_file.call_count, 1)
        self.assertEqual(
            mocked_task_debrid_and_save_file.call_args.kwargs,
            {"link": link, "folder": folder},
        )
        # Verify flask response
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(response.is_json)
        self.assertTrue(self.is_valid_uuid(response.json.get("task_id")))

    @patch(
        "megadebrid.worker.tasks.download_magnet.delay",
        return_value=MagicMock(id=uuid4()),
    )
    def test_megaweb_create_task_download_magnet(self, mocked_task_download_magnet):
        """
        Test that a request with header "Mega-Task: DownloadMagnet" on Flask correctly reaches
        download_magnet function of MegaWorker (celery task).
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
        folder = "/tmp"

        response = self.client.post(
            "/tasks",
            json={"magnet": magnet, "folder": folder},
            content_type="application/json",
            headers={"Mega-Task": "DownloadMagnet"},
        )

        # Verify celery task creation
        self.assertEqual(mocked_task_download_magnet.call_count, 1)
        self.assertEqual(
            mocked_task_download_magnet.call_args.kwargs,
            {"magnet": magnet, "folder": folder},
        )
        # Verify flask response
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(response.is_json)
        self.assertTrue(self.is_valid_uuid(response.json.get("task_id")))

    @patch(
        "megadebrid.worker.tasks.download_torrent.delay",
        return_value=MagicMock(id=uuid4()),
    )
    def test_megaweb_create_task_download_torrent(self, mocked_task_download_torrent):
        """
        Test that a request with header "Mega-Task: DownloadTorrent" on Flask correctly reaches
        download_torrent function of MegaWorker (celery task).
        """
        torrent_path = "/tmp/Rick.and.Morty.S06E01.WEBRip.mp4.torrent"
        folder = "/tmp"

        response = self.client.post(
            "/tasks",
            json={"torrent_path": torrent_path, "folder": folder},
            content_type="application/json",
            headers={"Mega-Task": "DownloadTorrent"},
        )

        # Verify celery task creation
        self.assertEqual(mocked_task_download_torrent.call_count, 1)
        self.assertEqual(
            mocked_task_download_torrent.call_args.kwargs,
            {"torrent_path": torrent_path, "folder": folder},
        )
        # Verify flask response
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(response.is_json)
        self.assertTrue(self.is_valid_uuid(response.json.get("task_id")))

    def test_megaweb_query_task_status(self):
        """
        Test that status requests will be correctly answered until completion or failure (JS behavior)
        """
        task_id = str(uuid4())

        # Patch flask instencied method "get_status" for route "/tasks/<task_id>"
        mock_status_response = MagicMock()
        mock_status_response.side_effect = [
            {"task_id": task_id, "task_status": "PENDING", "task_result": None},
            {"task_id": task_id, "task_status": "STARTED", "task_result": None},
            {"task_id": task_id, "task_status": "STARTED", "task_result": None},
            {
                "task_id": task_id,
                "task_status": "SUCCESS",
                "task_result": "/tmp/downloads/Rick.and.Morty.S06E01.WEBRip.mp4",
            },
        ]

        with patch.dict(
            self.app.view_functions, {"tasks.get_status": mock_status_response}
        ):
            response = self.client.get(f"tasks/{task_id}")

            # Verify flask response
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, "application/json")
            self.assertTrue(response.is_json)
            self.assertEqual(
                response.json,
                {"task_id": task_id, "task_status": "PENDING", "task_result": None},
            )

            # Waiting celery task to be completed or failed
            while response.json["task_status"] not in ["SUCCESS", "FAILURE"]:
                response = self.client.get(f"tasks/{task_id}")

            self.assertEqual(
                response.json,
                {
                    "task_id": task_id,
                    "task_status": "SUCCESS",
                    "task_result": "/tmp/downloads/Rick.and.Morty.S06E01.WEBRip.mp4",
                },
            )
