from argparse import ArgumentParser
from pathlib import Path


class MegaArgParser:
    @staticmethod
    def method_resolver(command):
        """Map the parsed command name (and its aliases) to the correct Mega-Object method name"""
        megafunc = {
            "connect-user": "connect_user",
            "connect": "connect_user",
            "user-history": "get_user_history",
            "history": "get_user_history",
            "hosters-list": "get_hosters_list",
            "hosters": "get_hosters_list",
            "my-torrents": "get_torrents_list",
            "list": "get_torrents_list",
            "torrents": "get_torrents_list",
            "torrent-status": "get_torrent_status",
            "status": "get_torrent_status",
            "upload-magnet": "upload_magnet",
            "magnet": "upload_magnet",
            "upload-torrent": "upload_torrent",
            "torrent": "upload_torrent",
            "remove-torrent": "remove_torrent",
            "remove": "remove_torrent",
            "debrid-link": "debrid_link",
            "debrid": "debrid_link",
            "link": "debrid_link",
            "wait-until-complete": "wait_until_complete",
            "wait": "wait_until_complete",
            "save-file": "save_file",
            "save": "save_file",
            "debrid-and-download": "debrid_and_save_file",
            "download": "debrid_and_save_file",
            "unrestrict": "debrid_and_save_file",
            "download-magnet": "download_magnet",
            "ddl-magnet": "download_magnet",
            "download-torrent": "download_torrent",
            "ddl-torrent": "download_torrent",
        }
        return megafunc[command]

    @staticmethod
    def create_parser():
        parser = ArgumentParser(
            description="Mega-CLI is the command line tool to interact with the different "
            "supported backends on Mega-Debrid.eu."
        )

        parser.add_argument(
            "-c",
            "--config",
            type=Path,
            default=Path.home() / ".mega" / "config",
            help="path for the config file (default: ~/.mega/config)",
        )

        subparsers = parser.add_subparsers(
            title="Mega-Debrid supported backends libs",
            help="choice of method to be use",
            required=True,
            dest="lib",
        )

        # Subparsers for MegaDebridAjax
        parser_ajax = subparsers.add_parser("ajax")

        subparser_ajax = parser_ajax.add_subparsers(
            title="Mega-AJAX commands",
            description="List of commands available on Mega-Debrid AJAX backend",
            required=True,
            dest="command",
        )

        # MegaDebridAjax: getMyTorrents
        parser_ajax_torrents_list = subparser_ajax.add_parser(
            "my-torrents",
            aliases=["list", "torrents"],
            help="get user torrents list",
        )
        # TODO: filter on STDOUT
        # parser_ajax_torrents_list.add_argument("--filter",
        #                                        type=str,
        #                                        dest="filter",
        #                                        default=None,
        #                                        help="filter results",
        # )

        # MegaDebridAjax: statusTorrent
        parser_ajax_torrent_status = subparser_ajax.add_parser(
            "torrent-status",
            aliases=["status"],
            help="get the status of a torrent",
        )
        parser_ajax_torrent_status.add_argument(
            "-i",
            "--id",
            metavar="ID",
            type=str,
            required=True,
            dest="torrent_id",
            help="ID of the torrent to query",
        )

        # MegaDebridAjax: uploadMagnet
        parser_ajax_upload_magnet = subparser_ajax.add_parser(
            "upload-magnet",
            aliases=["magnet"],
            help="add a magnet link",
        )
        parser_ajax_upload_magnet.add_argument(
            "magnet",
            metavar="MAGNET",
            type=str,
            help="link of the torrent magnet",
        )

        # MegaDebridAjax: uploadTorrent
        parser_ajax_upload_torrent = subparser_ajax.add_parser(
            "upload-torrent",
            aliases=["torrent"],
            help="Add a torrent file",
        )
        parser_ajax_upload_torrent.add_argument(
            "torrent",
            metavar="PATH",
            type=Path,
            help="path to the torrent file",
        )

        # MegaDebridAjax: removeTorrent
        parser_ajax_remove_torrent = subparser_ajax.add_parser(
            "remove-torrent",
            aliases=["remove"],
            help="remove a torrent from active torrents",
        )
        parser_ajax_remove_torrent.add_argument(
            "-i",
            "--id",
            metavar="ID",
            type=str,
            required=True,
            dest="torrent_id",
            help="ID of the torrent to remove",
        )

        # MegaDebridAjax: debridLink
        parser_ajax_debrid_link = subparser_ajax.add_parser(
            "debrid-link",
            aliases=["debrid", "link"],
            help="debrid links",
        )
        parser_ajax_debrid_link.add_argument(
            "link",
            metavar="URL",
            type=str,
            help="direct download link of the file to be debrided",
        )
        parser_ajax_debrid_link.add_argument(
            "-p",
            "--password",
            metavar="PASSWD",
            dest="password",
            type=str,
            help="if the link have password",
        )

        # Subparsers for MegaDebridApi
        parser_api = subparsers.add_parser("api")
        subparser_api = parser_api.add_subparsers(
            title="Mega-API commands",
            description="List of commands available on Mega-Debrid API backend",
            required=True,
            dest="command",
        )

        # MegaDebridApi: connectUser
        parser_api_connect_user = subparser_api.add_parser(
            "connect-user",
            aliases=["connect"],
            help="connect with creditials",
        )

        # MegaDebridApi: getUserHistory
        parser_api_user_history = subparser_api.add_parser(
            "user-history",
            aliases=["history"],
            help="get user download history",
        )

        # MegaDebridApi: getHostersList
        parser_api_hosters_list = subparser_api.add_parser(
            "hosters-list",
            aliases=["hosters"],
            help="list availables hosters (no authenticate)",
        )

        # MegaDebridApi: getTorrents
        parser_api_torrents_list = subparser_api.add_parser(
            "my-torrents",
            aliases=["list", "torrents"],
            help="get user torrents list",
        )
        # TODO: filter on STDOUT
        # parser_api_torrents_list.add_argument("--filter",
        #                                       type=str,
        #                                       dest="filter",
        #                                       default=None,
        #                                       help="filter results",
        # )

        # MegaDebridApi: getTorrent
        parser_api_torrent_status = subparser_api.add_parser(
            "torrent-status",
            aliases=["status"],
            help="get the status of selected torrent",
        )
        parser_api_torrent_status.add_argument(
            "--hash",
            metavar="HASH",
            type=str,
            required=True,
            dest="torrent_hash",
            help="hash of the torrent to query",
        )

        # MegaDebridApi: uploadTorrent (magnet)
        parser_api_upload_magnet = subparser_api.add_parser(
            "upload-magnet",
            aliases=["magnet"],
            help="add a magnet link",
        )
        parser_api_upload_magnet.add_argument(
            "magnet",
            metavar="MAGNET",
            type=str,
            help="link of the torrent magnet",
        )

        # MegaDebridApi: uploadTorrent (torrent file)
        parser_api_upload_torrent = subparser_api.add_parser(
            "upload-torrent",
            aliases=["torrent"],
            help="add a torrent file",
        )
        parser_api_upload_torrent.add_argument(
            "torrent",
            metavar="PATH",
            type=Path,
            help="path to the torrent file",
        )

        # MegaDebridApi: getLink
        parser_api_debrid_link = subparser_api.add_parser(
            "debrid-link",
            aliases=["debrid", "link"],
            help="debrided link",
        )
        parser_api_debrid_link.add_argument(
            "link",
            type=str,
            help="direct download link",
        )
        parser_api_debrid_link.add_argument(
            "-p",
            "--password",
            metavar="PASSWD",
            dest="password",
            type=str,
            help="if the link have password",
        )

        # Subparsers for MegaDebridFlow
        parser_flow = subparsers.add_parser("flow")
        subparser_flow = parser_flow.add_subparsers(
            title="Mega-Flow commands",
            description="List of commands available for Mega-Debrid advanced flow",
            required=True,
            dest="command",
        )

        # MegaDebridFlow: wait_until_complete
        subparser_flow_wait_complete = subparser_flow.add_parser(
            "wait-until-complete",
            aliases=["wait"],
            help="query the status of a torrent until it is completly processed by Torrent Converter",
        )
        subparser_flow_wait_complete.add_argument(
            "--hash",
            metavar="HASH",
            type=str,
            required=True,
            dest="torrent_hash",
            help="hash of the torrent to query",
        )
        subparser_flow_wait_complete.add_argument(
            "-s",
            "--second",
            metavar="SEC",
            dest="second",
            type=int,
            default=3,
            help="second to wait and each request of the status (default: 3)",
        )

        # MegaDebridFlow: save_file
        subparser_flow_save_file = subparser_flow.add_parser(
            "save-file",
            aliases=["save"],
            help="download the file at the given URL and save it in the specified folder",
        )
        subparser_flow_save_file.add_argument(
            "url",
            metavar="URL",
            type=str,
            help="URL of the file to download",
        )
        subparser_flow_save_file.add_argument(
            "-F",
            "--folder",
            metavar="PATH",
            dest="folder",
            type=Path,
            required=True,
            default=Path.home() / "Downloads",
            help="folder to save the file (default: ~/Downloads)",
        )
        subparser_flow_save_file.add_argument(
            "-f",
            "--filename",
            metavar="FILE",
            dest="filename",
            type=str,
            default=None,
            help="filename to save the file (default: None)",
        )
        subparser_flow_save_file.add_argument(
            "-c",
            "--chunk-size",
            metavar="SIZE",
            dest="chunk_size",
            type=int,
            default=1024 * 1024 * 10,
            help="size of the chunks while streaming the response (default: 10MB)",
        )
        subparser_flow_save_file.add_argument(
            "-b",
            "--progress-bar",
            metavar="BAR",
            dest="progress_bar",
            choices=[None, "bar", "size"],
            default=None,
            help="choose whether or not to display the progress bar and its type (default: None)",
        )

        # MegaDebridFlow: debrid_and_save_file
        subparser_flow_debrid_save = subparser_flow.add_parser(
            "debrid-and-download",
            aliases=["download", "unrestrict"],
            help="unrestrict the link and download it to the specified folder",
        )
        subparser_flow_debrid_save.add_argument(
            "link",
            type=str,
            help="direct download link",
        )
        subparser_flow_debrid_save.add_argument(
            "-p",
            "--password",
            metavar="PASSWD",
            dest="password",
            type=str,
            help="if the link have password",
        )
        subparser_flow_debrid_save.add_argument(
            "-F",
            "--folder",
            metavar="PATH",
            dest="folder",
            type=Path,
            default=Path.home() / "Downloads",
            help="folder to save the file (default: ~/Downloads)",
        )
        subparser_flow_debrid_save.add_argument(
            "-c",
            "--chunk-size",
            metavar="SIZE",
            dest="chunk_size",
            type=int,
            default=1024 * 1024 * 10,
            help="size of the chunks while streaming the response (default: 10MB)",
        )
        subparser_flow_debrid_save.add_argument(
            "-b",
            "--progress-bar",
            metavar="BAR",
            dest="progress_bar",
            choices=[None, "bar", "size"],
            default=None,
            help="choose whether or not to display the progress bar and its type (default: None)",
        )

        # MegaDebridFlow: download_magnet
        subparser_flow_download_magnet = subparser_flow.add_parser(
            "download-magnet",
            aliases=["ddl-magnet"],
            help="uses the torrent converter with a magnet link, "
            "then download the file in the specified folder",
        )
        subparser_flow_download_magnet.add_argument(
            "magnet",
            type=str,
            help="magnet link of the torrent",
        )
        subparser_flow_download_magnet.add_argument(
            "-F",
            "--folder",
            metavar="PATH",
            dest="folder",
            type=Path,
            default=Path.home() / "Downloads",
            help="folder to save the file (default: ~/Downloads)",
        )

        # MegaDebridFlow: download_torrent
        subparser_flow_download_torrent = subparser_flow.add_parser(
            "download-torrent",
            aliases=["ddl-torrent"],
            help="uses the torrent converter with a torrent file, "
            "then download the file in the specified folder",
        )
        subparser_flow_download_torrent.add_argument(
            "torrent_path",
            metavar="PATH",
            type=Path,
            help="path to the torrent file",
        )
        subparser_flow_download_torrent.add_argument(
            "-F",
            "--folder",
            metavar="PATH",
            dest="folder",
            type=Path,
            default=Path.home() / "Downloads",
            help="folder to save the file (default: ~/Downloads)",
        )

        return parser

    @classmethod
    def parse_args(cls):
        return cls.create_parser().parse_args()
