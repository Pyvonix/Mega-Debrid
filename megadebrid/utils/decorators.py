from functools import wraps
from inspect import signature


def renew_obsolete_token(method):
    """Catch obsolete token messe in response, than re-authenticate and re-execute function"""

    @wraps(method)
    async def wrapper_func(self, *method_args, **method_kwargs):
        response = await method(self, *method_args, **method_kwargs)

        # {"response_code": "TOKEN_ERROR", "response_text": "Token error, please log-in"}
        if response.get("response_code") == "TOKEN_ERROR":
            self.api_token = None
            await self.get_token(is_renew=True)
            response = await method(self, *method_args, **method_kwargs)

        return response

    # Make wrapped signature available
    wrapper_func.__signature__ = signature(method)

    return wrapper_func
