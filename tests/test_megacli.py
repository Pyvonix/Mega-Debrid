from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, mock_open
from importlib import import_module
from inspect import getfullargspec
from pathlib import Path

from megadebrid.parsers.argparser import MegaArgParser
from megadebrid.libs.ajax import MegaDebridAjax
from megadebrid.libs.flow import MegaDebridFlow
from megadebrid.libs.api import MegaDebridApi


@patch(
    "builtins.open",
    mock_open(read_data=open("tests/config.ini", "r", encoding="utf-8").read()),
)
class TestMegaCli(IsolatedAsyncioTestCase):
    """
    Test MegaCLI to reach the correct method on the related library
    """

    COMMANDS = [
        # MegaDebridAjax
        {
            # Command name: ajax_torrents_list
            "cli_args": ["ajax", "my-torrents"],
            "object": MegaDebridAjax,
            "func_mocked": "get_torrents_list",
            "expected_kwargs": {},
        },
        {
            # Command alias: ajax_torrents_list
            "cli_args": ["ajax", "list"],
            "object": MegaDebridAjax,
            "func_mocked": "get_torrents_list",
            "expected_kwargs": {},
        },
        {
            # Command alias 2: ajax_torrents_list
            "cli_args": ["ajax", "torrents"],
            "object": MegaDebridAjax,
            "func_mocked": "get_torrents_list",
            "expected_kwargs": {},
        },
        {
            # Command name: ajax_torrent_status
            "cli_args": ["ajax", "torrent-status", "--id", "12345"],
            "object": MegaDebridAjax,
            "func_mocked": "get_torrent_status",
            "expected_kwargs": {"torrent_id": "12345"},
        },
        {
            # Command alias: ajax_torrent_status
            "cli_args": ["ajax", "status", "-i", "12345"],
            "object": MegaDebridAjax,
            "func_mocked": "get_torrent_status",
            "expected_kwargs": {"torrent_id": "12345"},
        },
        {
            # Command name: ajax_upload_magnet
            "cli_args": [
                "ajax",
                "upload-magnet",
                "magnet:?xt=urn:btih:fb72d751bcc437746583c298ce395b84f3089e8f"
                "&dn=Rick.and.Morty.S06E01.WEBRip.mp4"
                "&tr=http%3A%2F%2Fexample.tracker.wf%3A7777%2Fannounce"
                "&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce"
                "&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce",
            ],
            "object": MegaDebridAjax,
            "func_mocked": "upload_magnet",
            "expected_kwargs": {
                "magnet": "magnet:?xt=urn:btih:fb72d751bcc437746583c298ce395b84f3089e8f"
                "&dn=Rick.and.Morty.S06E01.WEBRip.mp4"
                "&tr=http%3A%2F%2Fexample.tracker.wf%3A7777%2Fannounce"
                "&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce"
                "&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce"
            },
        },
        {
            # Command alias: ajax_upload_magnet
            "cli_args": [
                "ajax",
                "magnet",
                "magnet:?xt=urn:btih:fb72d751bcc437746583c298ce395b84f3089e8f"
                "&dn=Rick.and.Morty.S06E01.WEBRip.mp4"
                "&tr=http%3A%2F%2Fexample.tracker.wf%3A7777%2Fannounce"
                "&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce"
                "&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce",
            ],
            "object": MegaDebridAjax,
            "func_mocked": "upload_magnet",
            "expected_kwargs": {
                "magnet": "magnet:?xt=urn:btih:fb72d751bcc437746583c298ce395b84f3089e8f"
                "&dn=Rick.and.Morty.S06E01.WEBRip.mp4"
                "&tr=http%3A%2F%2Fexample.tracker.wf%3A7777%2Fannounce"
                "&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce"
                "&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce"
            },
        },
        {
            # Command name: ajax_upload_torrent
            "cli_args": [
                "ajax",
                "upload-torrent",
                "/tmp/Rick.and.Morty.S06E01.WEBRip.mp4.torrent",
            ],
            "object": MegaDebridAjax,
            "func_mocked": "upload_torrent",
            "expected_kwargs": {
                "torrent": Path("/tmp/Rick.and.Morty.S06E01.WEBRip.mp4.torrent")
            },
        },
        {
            # Command alias: ajax_upload_torrent
            "cli_args": [
                "ajax",
                "torrent",
                "/tmp/Rick.and.Morty.S06E01.WEBRip.mp4.torrent",
            ],
            "object": MegaDebridAjax,
            "func_mocked": "upload_torrent",
            "expected_kwargs": {
                "torrent": Path("/tmp/Rick.and.Morty.S06E01.WEBRip.mp4.torrent")
            },
        },
        {
            # Command alias: ajax_remove_torrent
            "cli_args": ["ajax", "remove-torrent", "--id", "12345"],
            "object": MegaDebridAjax,
            "func_mocked": "remove_torrent",
            "expected_kwargs": {"torrent_id": "12345"},
        },
        {
            # Command alias: ajax_remove_torrent
            "cli_args": ["ajax", "remove", "-i", "12345"],
            "object": MegaDebridAjax,
            "func_mocked": "remove_torrent",
            "expected_kwargs": {"torrent_id": "12345"},
        },
        {
            # Command name: ajax_debrid_link
            "cli_args": [
                "ajax",
                "debrid-link",
                "https://1fichier.com/?AAAAAAAAAAAAAAAAAAAA",
            ],
            "object": MegaDebridAjax,
            "func_mocked": "debrid_link",
            "expected_kwargs": {
                "link": "https://1fichier.com/?AAAAAAAAAAAAAAAAAAAA",
                "password": None,
            },
        },
        {
            # Command name: ajax_debrid_link
            "cli_args": [
                "ajax",
                "debrid",
                "https://1fichier.com/?AAAAAAAAAAAAAAAAAAAA",
            ],
            "object": MegaDebridAjax,
            "func_mocked": "debrid_link",
            "expected_kwargs": {
                "link": "https://1fichier.com/?AAAAAAAAAAAAAAAAAAAA",
                "password": None,
            },
        },
        {
            # Command alias 2: ajax_debrid_link
            "cli_args": ["ajax", "link", "https://1fichier.com/?AAAAAAAAAAAAAAAAAAAA"],
            "object": MegaDebridAjax,
            "func_mocked": "debrid_link",
            "expected_kwargs": {
                "link": "https://1fichier.com/?AAAAAAAAAAAAAAAAAAAA",
                "password": None,
            },
        },
        # MegaDebridAPi
        {
            # Command name: api_connect_user
            "cli_args": ["api", "connect-user"],
            "object": MegaDebridApi,
            "func_mocked": "connect_user",
            "expected_kwargs": {},
        },
        {
            # Command alias: api_connect_user
            "cli_args": ["api", "connect"],
            "object": MegaDebridApi,
            "func_mocked": "connect_user",
            "expected_kwargs": {},
        },
        {
            # Command name: api_user_history
            "cli_args": ["api", "user-history"],
            "object": MegaDebridApi,
            "func_mocked": "get_user_history",
            "expected_kwargs": {},
        },
        {
            # Command alias: api_user_history
            "cli_args": ["api", "history"],
            "object": MegaDebridApi,
            "func_mocked": "get_user_history",
            "expected_kwargs": {},
        },
        {
            # Command alias: api_hosters_list
            "cli_args": ["api", "hosters-list"],
            "object": MegaDebridApi,
            "func_mocked": "get_hosters_list",
            "expected_kwargs": {},
        },
        {
            # Command alias: api_hosters_list
            "cli_args": ["api", "hosters"],
            "object": MegaDebridApi,
            "func_mocked": "get_hosters_list",
            "expected_kwargs": {},
        },
        {
            # Command name: api_torrents_list
            "cli_args": ["api", "my-torrents"],
            "object": MegaDebridApi,
            "func_mocked": "get_torrents_list",
            "expected_kwargs": {},
        },
        {
            # Command alias: api_torrents_list
            "cli_args": ["api", "list"],
            "object": MegaDebridApi,
            "func_mocked": "get_torrents_list",
            "expected_kwargs": {},
        },
        {
            # Command alias 2: api_torrents_list
            "cli_args": ["api", "torrents"],
            "object": MegaDebridApi,
            "func_mocked": "get_torrents_list",
            "expected_kwargs": {},
        },
        {
            # Command name: api_torrent_status
            "cli_args": [
                "api",
                "torrent-status",
                "--hash",
                "fb72d751bcc437746583c298ce395b84f3089e8f",
            ],
            "object": MegaDebridApi,
            "func_mocked": "get_torrent_status",
            "expected_kwargs": {
                "torrent_hash": "fb72d751bcc437746583c298ce395b84f3089e8f"
            },
        },
        {
            # Command alias: api_torrent_status
            "cli_args": [
                "api",
                "status",
                "--hash",
                "fb72d751bcc437746583c298ce395b84f3089e8f",
            ],
            "object": MegaDebridApi,
            "func_mocked": "get_torrent_status",
            "expected_kwargs": {
                "torrent_hash": "fb72d751bcc437746583c298ce395b84f3089e8f"
            },
        },
        {
            # Command name: api_upload_magnet
            "cli_args": [
                "api",
                "magnet",
                "magnet:?xt=urn:btih:fb72d751bcc437746583c298ce395b84f3089e8f"
                "&dn=Rick.and.Morty.S06E01.WEBRip.mp4"
                "&tr=http%3A%2F%2Fexample.tracker.wf%3A7777%2Fannounce"
                "&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce"
                "&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce",
            ],
            "object": MegaDebridApi,
            "func_mocked": "upload_magnet",
            "expected_kwargs": {
                "magnet": "magnet:?xt=urn:btih:fb72d751bcc437746583c298ce395b84f3089e8f"
                "&dn=Rick.and.Morty.S06E01.WEBRip.mp4"
                "&tr=http%3A%2F%2Fexample.tracker.wf%3A7777%2Fannounce"
                "&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce"
                "&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce"
            },
        },
        {
            # Command alias: api_upload_magnet
            "cli_args": [
                "api",
                "magnet",
                "magnet:?xt=urn:btih:fb72d751bcc437746583c298ce395b84f3089e8f"
                "&dn=Rick.and.Morty.S06E01.WEBRip.mp4"
                "&tr=http%3A%2F%2Fexample.tracker.wf%3A7777%2Fannounce"
                "&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce"
                "&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce",
            ],
            "object": MegaDebridApi,
            "func_mocked": "upload_magnet",
            "expected_kwargs": {
                "magnet": "magnet:?xt=urn:btih:fb72d751bcc437746583c298ce395b84f3089e8f"
                "&dn=Rick.and.Morty.S06E01.WEBRip.mp4"
                "&tr=http%3A%2F%2Fexample.tracker.wf%3A7777%2Fannounce"
                "&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce"
                "&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce"
            },
        },
        {
            # Command name: api_upload_torrent
            "cli_args": [
                "api",
                "upload-torrent",
                "/tmp/Rick.and.Morty.S06E01.WEBRip.mp4.torrent",
            ],
            "object": MegaDebridApi,
            "func_mocked": "upload_torrent",
            "expected_kwargs": {
                "torrent": Path("/tmp//Rick.and.Morty.S06E01.WEBRip.mp4.torrent")
            },
        },
        {
            # Command alias: api_upload_torrent
            "cli_args": [
                "api",
                "upload-torrent",
                "/tmp/Rick.and.Morty.S06E01.WEBRip.mp4.torrent",
            ],
            "object": MegaDebridApi,
            "func_mocked": "upload_torrent",
            "expected_kwargs": {
                "torrent": Path("/tmp/Rick.and.Morty.S06E01.WEBRip.mp4.torrent")
            },
        },
        {
            # Command name: api_debrid_link
            "cli_args": [
                "api",
                "debrid-link",
                "https://1fichier.com/?AAAAAAAAAAAAAAAAAAAA",
            ],
            "object": MegaDebridApi,
            "func_mocked": "debrid_link",
            "expected_kwargs": {
                "link": "https://1fichier.com/?AAAAAAAAAAAAAAAAAAAA",
                "password": None,
            },
        },
        {
            # Command alias: api_debrid_link
            "cli_args": ["api", "debrid", "https://1fichier.com/?AAAAAAAAAAAAAAAAAAAA"],
            "object": MegaDebridApi,
            "func_mocked": "debrid_link",
            "expected_kwargs": {
                "link": "https://1fichier.com/?AAAAAAAAAAAAAAAAAAAA",
                "password": None,
            },
        },
        {
            # Command alias 2: api_debrid_link
            "cli_args": ["api", "link", "https://1fichier.com/?AAAAAAAAAAAAAAAAAAAA"],
            "object": MegaDebridApi,
            "func_mocked": "debrid_link",
            "expected_kwargs": {
                "link": "https://1fichier.com/?AAAAAAAAAAAAAAAAAAAA",
                "password": None,
            },
        },
        # MegaDebridFlow
        {
            # Command name: flow_wait_complete
            "cli_args": [
                "flow",
                "wait-until-complete",
                "--hash",
                "fb72d751bcc437746583c298ce395b84f3089e8f",
            ],
            "object": MegaDebridFlow,
            "func_mocked": "wait_until_complete",
            "expected_kwargs": {
                "torrent_hash": "fb72d751bcc437746583c298ce395b84f3089e8f",
                "second": 3,
            },
        },
        {
            # Command name: flow_wait_complete
            "cli_args": [
                "flow",
                "wait",
                "--hash",
                "fb72d751bcc437746583c298ce395b84f3089e8f",
            ],
            "object": MegaDebridFlow,
            "func_mocked": "wait_until_complete",
            "expected_kwargs": {
                "torrent_hash": "fb72d751bcc437746583c298ce395b84f3089e8f",
                "second": 3,
            },
        },
        {
            # Command name: flow_save_file
            "cli_args": [
                "flow",
                "save-file",
                "--folder",
                "/tmp/downloads",
                "https://file-examples.com/storage/feeb72b10363daaeba4c0c9/2017/10/file_example_PNG_1MB.png",
            ],
            "object": MegaDebridFlow,
            "func_mocked": "save_file",
            "expected_kwargs": {
                "url": "https://file-examples.com/storage/feeb72b10363daaeba4c0c9/2017/10/file_example_PNG_1MB.png",
                "folder": Path("/tmp/downloads"),
                "filename": None,
                "chunk_size": 1024 * 1024 * 10,
                "progress_bar": None,
            },
        },
        {
            # Command alias: flow_save_file
            "cli_args": [
                "flow",
                "save",
                "--folder",
                "/tmp/downloads",
                "https://file-examples.com/storage/feeb72b10363daaeba4c0c9/2017/10/file_example_PNG_1MB.png",
            ],
            "object": MegaDebridFlow,
            "func_mocked": "save_file",
            "expected_kwargs": {
                "url": "https://file-examples.com/storage/feeb72b10363daaeba4c0c9/2017/10/file_example_PNG_1MB.png",
                "folder": Path("/tmp/downloads"),
                "filename": None,
                "chunk_size": 1024 * 1024 * 10,
                "progress_bar": None,
            },
        },
        {
            # Command name: flow_debrid_and_save_file
            "cli_args": [
                "flow",
                "debrid-and-download",
                "--folder",
                "/tmp/downloads",
                "https://1fichier.com/?AAAAAAAAAAAAAAAAAAAA",
            ],
            "object": MegaDebridFlow,
            "func_mocked": "debrid_and_save_file",
            "expected_kwargs": {
                "link": "https://1fichier.com/?AAAAAAAAAAAAAAAAAAAA",
                "folder": Path("/tmp/downloads"),
                "password": None,
                "chunk_size": 1024 * 1024 * 10,
                "progress_bar": None,
            },
        },
        {
            # Command alias: flow_debrid_and_save_file
            "cli_args": [
                "flow",
                "unrestrict",
                "-F",
                "/tmp/downloads",
                "https://1fichier.com/?AAAAAAAAAAAAAAAAAAAA",
            ],
            "object": MegaDebridFlow,
            "func_mocked": "debrid_and_save_file",
            "expected_kwargs": {
                "link": "https://1fichier.com/?AAAAAAAAAAAAAAAAAAAA",
                "folder": Path("/tmp/downloads"),
                "password": None,
                "chunk_size": 1024 * 1024 * 10,
                "progress_bar": None,
            },
        },
        {
            # Command alias 2: flow_debrid_and_save_file
            "cli_args": [
                "flow",
                "download",
                "-F",
                "/tmp/downloads",
                "https://1fichier.com/?AAAAAAAAAAAAAAAAAAAA",
            ],
            "object": MegaDebridFlow,
            "func_mocked": "debrid_and_save_file",
            "expected_kwargs": {
                "link": "https://1fichier.com/?AAAAAAAAAAAAAAAAAAAA",
                "folder": Path("/tmp/downloads"),
                "password": None,
                "chunk_size": 1024 * 1024 * 10,
                "progress_bar": None,
            },
        },
        {
            # Command name: flow_download_magnet
            "cli_args": [
                "flow",
                "download-magnet",
                "--folder",
                "/tmp/downloads",
                "magnet:?xt=urn:btih:fb72d751bcc437746583c298ce395b84f3089e8f"
                "&dn=Rick.and.Morty.S06E01.WEBRip.mp4"
                "&tr=http%3A%2F%2Fexample.tracker.wf%3A7777%2Fannounce"
                "&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce"
                "&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce",
            ],
            "object": MegaDebridFlow,
            "func_mocked": "download_magnet",
            "expected_kwargs": {
                "magnet": "magnet:?xt=urn:btih:fb72d751bcc437746583c298ce395b84f3089e8f"
                "&dn=Rick.and.Morty.S06E01.WEBRip.mp4"
                "&tr=http%3A%2F%2Fexample.tracker.wf%3A7777%2Fannounce"
                "&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce"
                "&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce",
                "folder": Path("/tmp/downloads"),
            },
        },
        {
            # Command alias: flow_download_magnet
            "cli_args": [
                "flow",
                "ddl-magnet",
                "--folder",
                "/tmp/downloads",
                "magnet:?xt=urn:btih:fb72d751bcc437746583c298ce395b84f3089e8f"
                "&dn=Rick.and.Morty.S06E01.WEBRip.mp4"
                "&tr=http%3A%2F%2Fexample.tracker.wf%3A7777%2Fannounce"
                "&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce"
                "&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce",
            ],
            "object": MegaDebridFlow,
            "func_mocked": "download_magnet",
            "expected_kwargs": {
                "magnet": "magnet:?xt=urn:btih:fb72d751bcc437746583c298ce395b84f3089e8f"
                "&dn=Rick.and.Morty.S06E01.WEBRip.mp4"
                "&tr=http%3A%2F%2Fexample.tracker.wf%3A7777%2Fannounce"
                "&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce"
                "&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce"
                "&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce",
                "folder": Path("/tmp/downloads"),
            },
        },
        {
            # Command name: flow_download_torrent
            "cli_args": [
                "flow",
                "download-torrent",
                "--folder",
                "/tmp/downloads",
                "/tmp/Rick.and.Morty.S06E01.WEBRip.mp4.torrent",
            ],
            "object": MegaDebridFlow,
            "func_mocked": "download_torrent",
            "expected_kwargs": {
                "torrent_path": Path("/tmp/Rick.and.Morty.S06E01.WEBRip.mp4.torrent"),
                "folder": Path("/tmp/downloads"),
            },
        },
        {
            # Command alias: flow_download_torrent
            "cli_args": [
                "flow",
                "ddl-torrent",
                "--folder",
                "/tmp/downloads",
                "/tmp/Rick.and.Morty.S06E01.WEBRip.mp4.torrent",
            ],
            "object": MegaDebridFlow,
            "func_mocked": "download_torrent",
            "expected_kwargs": {
                "torrent_path": Path("/tmp/Rick.and.Morty.S06E01.WEBRip.mp4.torrent"),
                "folder": Path("/tmp/downloads"),
            },
        },
    ]

    def setUp(self):
        super().setUp()
        self.parser = MegaArgParser.create_parser()
        self.MegaCLI = import_module("mega-cli").MegaCLI

    @patch("megadebrid.parsers.argparser.MegaArgParser.parse_args")
    async def test_megacli_commands(self, mocked_parse_args):
        """
        Test mega-cli commands on the different backend verifying that the arguments are passed to the right functions
        """

        for cmd_test in self.COMMANDS:
            with self.subTest(
                msg=f'Testing with args: { " ".join(cmd_test["cli_args"]) }'
            ):
                # Mega-cli: parse args command
                mocked_parse_args.return_value = self.parser.parse_args(
                    cmd_test["cli_args"]
                )

                megacli = self.MegaCLI()
                # First call of the object method SHOULD NOT be mocked: therefore
                # reproduce the original behavior of 'getfullargspec'
                with patch(
                    "mega-cli.getfullargspec",
                    return_value=getfullargspec(
                        getattr(cmd_test["object"], cmd_test["func_mocked"])
                    ),
                ):
                    with patch.object(
                        cmd_test["object"], cmd_test["func_mocked"]
                    ) as mocked_megalib_obj_func:
                        await megacli.async_run()
                        self.assertEqual(mocked_megalib_obj_func.call_count, 1)
                        self.assertEqual(
                            mocked_megalib_obj_func.call_args.kwargs,
                            cmd_test["expected_kwargs"],
                        )
