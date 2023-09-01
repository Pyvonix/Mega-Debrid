import asyncio
from pathlib import Path
from typing import Optional

from aiofiles import open as aiopen
from urllib.parse import urlparse, parse_qs, unquote_plus

from megadebrid.utils.progressions import Progress
from megadebrid.libs.api import MegaDebridApi


class MegaDebridFlow(MegaDebridApi):
    """
    Mega-Debrid Flow: provide an advanced usage of the MegaDebridApi,
    to perform a chain the actions to obtain the desired beahvior.
    """

    def __init__(self, *args, **kwargs) -> None:
        # flow = kwargs.pop('flow', 'api')
        super().__init__()
        self.progress = Progress()

    @staticmethod
    def get_magnet_hash(magnet: str) -> str:
        """Mega-Debrid API seems doesn't return magnet hash... Then query it inside magnet"""
        parsed_magnet = urlparse(magnet)
        magnet_qs = parse_qs(parsed_magnet.query)
        return magnet_qs["xt"][0][len("urn:btih:") :]

    @staticmethod
    def path_exists(path: str) -> Path:
        if not path:
            return Path.home() / "Downloads"

        path = Path(path)
        if not path.exists():
            print(f"cannot access '{ path }': No such file or directory")
            exit(1)
        return path

    async def wait_until_complete(self, torrent_hash: str, second: int = 3) -> dict:
        """
        Request the torrent status until upload is complete

        Args:
            torrent_hash (str): Torrent hash to monitor.
            second (int, optional): Second to wait between each request. Defaults to 1.

        Returns:
            dict: Return last the torrent status response which is complete
        """
        json_rep = await self.get_torrent_status(torrent_hash)

        while json_rep["status"]["status"] != "complete":
            await asyncio.sleep(second)
            json_rep = await self.get_torrent_status(torrent_hash)

            print(json_rep["status"])
            # end='\r' if json_rep['status']['status'] != 'complete' else '\n')            # will change size when printing

        return json_rep

    async def save_file(
        self,
        url: str,
        folder: Path,
        filename: Optional[str] = None,
        chunk_size: int = 1024 * 1024 * 10,
        progress_bar: Optional[str] = None,
    ) -> Path:
        """
        Asynchronous downloading and saving of the remote file

        Args:
            url (str): URL of the file to download.
            folder (Path): Folder to save the file that will be downloaded.
            filename (str): Filename to save on the local disk.
            chunk_size (int, optional): Size of the chunks while streaming the response. Defaults to 10MB.
            progress_bar (str, optional): Name of the show_progress wishes: None, bar or size. Default to None.

        Returns:
            Path: Path of the saved file
        """
        folder = (
            folder if isinstance(folder, Path) else Path(folder)
        )  # ? PREVENT ANY PROBLEM YET

        async with self.session.get(url) as response:
            content_length = int(response.headers.get("Content-Length", 0))
            filename = filename or unquote_plus(url.rsplit("/", 1)[-1])

            async with aiopen(folder / filename, "wb") as f:
                chunk_written = 0

                async for chunk in response.content.iter_chunked(chunk_size):
                    await f.write(chunk)

                    if progress_bar:
                        chunk_written += chunk_size
                        self.progress.render(
                            progress=chunk_written, total=content_length, choice="bar"
                        )

                await f.flush()

        return folder / filename

    async def debrid_and_save_file(
        self,
        link: str,
        folder: Path,
        password: str = "",
        chunk_size: int = 1024 * 1024 * 10,
        progress_bar: str = None,
    ) -> Path:
        """
        Debride the file/link and download it to the specified folder.
        It's the equivalent of 'unrestrict my links' feature on Mega-Debrid.eu.

        Args:
            link (str): direct download link.
            folder (Path): folder to save the file.
            password (str, optional): if the link have password. Defaults to "".
            chunk_size (int, optional): Size of the chunks while streaming the response. Defaults to 10MB.
            progress_bar (str or None, optional): Name of the show_progress wishes: None, bar or size. Default to None.

        Returns:
            str: Path of the downloaded file
        """
        json_rep = await self.debrid_link(link, password)
        saved_path = await self.save_file(
            url=json_rep["debridLink"],
            folder=folder,
            filename=json_rep["filename"],
            chunk_size=chunk_size,
            progress_bar=progress_bar,
        )

        return saved_path

    async def download_magnet(self, magnet: str, folder: Path) -> Path:
        """
        Uses the torrent converter with a magnet link,
        then download the file in the specified folder.

        Args:
            magnet (str): magnet link of the torrent.
            folder (Path): folder to save the file.

        Returns:
            Path: Path of the downloaded file
        """
        json_rep = await self.upload_magnet(magnet)
        torrent_hash = json_rep["newTorrent"]["hash"] or self.get_magnet_hash(magnet)

        json_rep = await self.wait_until_complete(torrent_hash)
        saved_path = await self.debrid_and_save_file(
            link=json_rep["status"]["ub_link"], folder=folder
        )

        return saved_path

    async def download_torrent(self, torrent_path: Path, folder: Path) -> Path:
        """
        Uses the torrent converter with a torrent file,
        then download the file in the specified folder.

        Args:
            torrent_path (Path): path of the torrent file.
            folder (Path): folder to save the file.

        Returns:
            Path: Path of the downloaded file
        """
        print(type(torrent_path), torrent_path)
        json_rep = await self.upload_torrent(torrent_path)
        torrent_hash = json_rep["newTorrent"]["hash"]

        json_rep = await self.wait_until_complete(torrent_hash)
        saved_path = await self.debrid_and_save_file(
            link=json_rep["status"]["ub_link"], folder=folder
        )

        return saved_path
