import asyncio
from pathlib import Path
from typing import Any

from .celery import app as celery_app
from megadebrid.libs.flow import MegaDebridFlow


def serializer(obj: Any):
    """Require result serializer"""
    if isinstance(obj, Path):
        return str(obj)
    return obj


async def async_wrapper(func_name, **kwargs) -> Any:
    """
    Celery doesn't support yet direct asynchronous task, it requires to wrap asyncio methods.

    > celery 6 will mainly focus on asyncio support. but as you all can see you can't do that before Q1 2023.
    Source: https://github.com/celery/celery/issues/6552

    Args:
        func_name (str): the method in MegaDebridFlow which will be handled as celery task

    Returns:
        any: the type for each of the MegaDebridFlow functions. Mainly Paths that need to be
             serialized to be stored as JSON result by celery.
    """
    async with MegaDebridFlow() as megadebrid:
        result = await getattr(megadebrid, func_name)(**kwargs)
        return serializer(result)


@celery_app.task(name="save_file")
def save_file(url: str, folder: Path):
    """Call the async_wrapper to handle the MegaDebridFlow method 'save_file' as synchronous task"""
    result = asyncio.run(async_wrapper(func_name="save_file", url=url, folder=folder))
    return result


@celery_app.task(name="debrid_and_save_file")
def debrid_and_save_file(link: str, folder: Path, password: str = ""):
    """Call the async_wrapper to handle the MegaDebridFlow method 'debrid_and_save_file' as synchronous task"""
    result = asyncio.run(
        async_wrapper(
            func_name="debrid_and_save_file",
            link=link,
            folder=folder,
            password=password,
        )
    )
    return result


@celery_app.task(name="download_magnet")
def download_magnet(magnet: str, folder: Path):
    """Call the async_wrapper to handle the MegaDebridFlow method 'download_magnet' as synchronous task"""
    result = asyncio.run(
        async_wrapper(func_name="download_magnet", magnet=magnet, folder=folder)
    )
    return result


@celery_app.task(name="download_torrent")
def download_torrent(torrent_path: Path, folder: Path):
    """Call the async_wrapper to handle the MegaDebridFlow method 'download_torrent' as synchornous task"""
    result = asyncio.run(
        async_wrapper(
            func_name="download_torrent", torrent_path=torrent_path, folder=folder
        )
    )
    return result
