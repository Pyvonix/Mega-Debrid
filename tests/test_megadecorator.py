from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, mock_open
from aioresponses import aioresponses

from megadebrid.libs.api import MegaDebridApi


@patch(
    "builtins.open",
    mock_open(read_data=open("tests/config.ini", "r", encoding="utf-8").read()),
)
class TestMegaDecorator(IsolatedAsyncioTestCase):
    """
    Test available decorators on Mega-Debrid project
    """

    @aioresponses()
    async def test_renew_token(self, mocked):
        """
        Test to perform an action on Mega-Debrid API while token is exprired and need to be renew.
        decorator: @renew_obsolete_token is involked
        """

        mocked.add(
            method="GET",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=getUserHistory&token=XXXXXXXXXXXXXXXXXXXXXXXXXX",
            content_type="text/html; charset=UTF-8",
            payload={
                "response_code": "TOKEN_ERROR",
                "response_text": "Token error, please log-in",
            },
        )
        mocked.add(
            method="GET",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=connectUser&login=user&password=password",
            content_type="text/html; charset=UTF-8",
            payload={
                "response_code": "ok",
                "response_text": "User logged",
                "token": "YYYYYYYYYYYYYYYYYYYYYYYYYY",
                "vip_end": "1111111111",
                "email": "user@example.com",
            },
        )
        mocked.add(
            method="GET",
            status=200,
            url="https://www.mega-debrid.eu/api.php?action=getUserHistory&token=YYYYYYYYYYYYYYYYYYYYYYYYYY",
            content_type="text/html; charset=UTF-8",
            payload={"response_code": "ok", "response_text": "", "history": []},
        )

        async with MegaDebridApi() as megadebrid:
            response = await megadebrid.get_user_history()

        self.assertEqual(response["response_code"], "ok")
        self.assertIsInstance(response["history"], list)
