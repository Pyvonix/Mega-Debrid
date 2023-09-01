from typing import Optional

from configparser import ConfigParser
from pathlib import Path
from json import loads
from os import getenv


class MegaConfigParser(ConfigParser):
    DEFAULT_PATH = Path.home() / ".mega" / "config"
    # CREDENTIALS environment variables
    ENV_VAR_USER = "MEGA_USER"
    ENV_VAR_PASSWD = "MEGA_PASSWD"
    # API environment variables
    ENV_VAR_API = "MEGA_TOKEN"
    # AJAX environment variables
    ENV_VAR_USER_AGENT = "MEGA_USER_AGENT"
    ENV_VAR_COOKIES = "MEGA_COOKIES"

    def __init__(self, config_path=None) -> None:
        super().__init__()
        self.optionxform = str  # Preserve case in ConfigParser
        config_path = config_path or self.DEFAULT_PATH
        self.read(config_path)

    def read_credentials_envvars(self) -> dict:
        """Read credentials from environment variables"""
        env_credentials = {
            "Username": getenv(self.ENV_VAR_USER),
            "Password": getenv(self.ENV_VAR_PASSWD),
        }
        return env_credentials if all(env_credentials.values()) else {}

    def read_credentials_config(self) -> dict:
        """Read credentials from config file"""
        return (
            dict(self["CREDENTIALS"].items()) if self.has_section("CREDENTIALS") else {}
        )

    def get_credentials(self) -> dict:
        return self.read_credentials_envvars() or self.read_credentials_config()

    def read_ajax_envvars(self) -> tuple[Optional[str], dict]:
        """Read AJAX USER-AGENT & COOKIES from environment variables"""
        return getenv(self.ENV_VAR_USER_AGENT), loads(
            getenv(self.ENV_VAR_COOKIES, "{}")
        )

    def read_ajax_config(self) -> tuple[Optional[str], dict]:
        """Read AJAX USER-AGENT & COOKIES from config file"""
        if self.has_section("AJAX"):
            ajax_dict = dict(self["AJAX"].items())
            user_agent = ajax_dict.pop("USER-AGENT", None)
            return user_agent, ajax_dict
        return None, {}

    def get_ajax_info(self) -> dict[str, str]:
        """Deal between AJAX environment variable and config"""
        envvars_user_agent, envvars_cookies = self.read_ajax_envvars()
        config_user_agent, config_cookies = self.read_ajax_config()
        return {
            "USER-AGENT": envvars_user_agent or config_user_agent,
            "COOKIES": envvars_cookies or config_cookies,
        }

    def export_api_envvars(self) -> dict:
        """Export API from environment variables"""
        raise NotImplementedError

    def read_api_envvars(self) -> Optional[str]:
        """Read API from environment variables"""
        return getenv(self.ENV_VAR_API, None)

    def write_api_config(self) -> dict:
        """Read API from config file"""
        raise NotImplementedError

    def read_api_config(self) -> Optional[str]:
        """Read API from config file"""
        return self["API"].get("TOKEN") if self.has_section("API") else None

    def get_api_token(self) -> Optional[str]:
        """Deal between environment variable and config API"""
        return self.read_api_envvars() or self.read_api_config()

    def save_api_token(self, token) -> None:
        if "^Token =" in "":
            pass
            # config.has_section('API')
            # config.has_option('API', 'TOKEN')
        else:
            f"Token = {token}"
