from megadebrid.libs.api import MegaDebridApi
from megadebrid.libs.ajax import MegaDebridAjax
from megadebrid.libs.flow import MegaDebridFlow
from megadebrid.parsers.argparser import MegaArgParser

from inspect import getfullargspec
import asyncio
import signal


class MegaCLI:
    def __init__(self) -> None:
        self.args = MegaArgParser.parse_args()
        self.objects = {
            "ajax": MegaDebridAjax,
            "api": MegaDebridApi,
            "flow": MegaDebridFlow,
        }
        self.SIGINT = False

    def signal_handler(self, signal, frame) -> None:
        print("\n MegaCLI has been interrupted!!")
        self.SIGINT = True

    async def run_until_interrupt(self, func, *args, **kwargs) -> None:
        signal.signal(signal.SIGINT, self.signal_handler)

        while not self.SIGINT:
            await func(*args, **kwargs)
            await asyncio.sleep(3)

    async def async_run(self) -> None:
        async with self.objects[self.args.lib]() as megadebrid:
            megadebrid_method = getattr(
                megadebrid, MegaArgParser.method_resolver(self.args.command)
            )

            method_args = set(getfullargspec(megadebrid_method).args[1:])
            require_args = {
                key: value
                for key, value in vars(self.args).items()
                if key in method_args
            }
            result = await megadebrid_method(**require_args)
            print(result)

            # TODO: need to be implemented
            # await a.run_until_interrupt('none')


if __name__ == "__main__":
    megacli = MegaCLI()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(megacli.async_run())
    loop.close()
