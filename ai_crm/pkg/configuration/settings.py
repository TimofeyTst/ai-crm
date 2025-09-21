import pathlib
import typing
import urllib.parse

from pydantic import field_validator
from pydantic.types import PositiveInt, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv

from ai_crm.pkg.models import logger

class Postgresql(BaseSettings):
    HOSTS: typing.Optional[str] = None
    PORT: PositiveInt = 5432
    USER: str = "postgres"
    PASSWORD: SecretStr = SecretStr("postgres")
    DATABASE_NAME: str = "postgres"

    MIN_CONNECTION: PositiveInt = 1
    MAX_CONNECTION: PositiveInt = 16

    def get_hosts_list(self) -> typing.List[str]:
        if self.HOSTS:
            return [host.strip() for host in self.HOSTS.split(',')]
        return [self.HOST]
    
    def build_dsn_for_host(self, host: str) -> str:
        password = self.PASSWORD.get_secret_value() if self.PASSWORD else ''
        return f"postgresql://{self.USER}:{urllib.parse.quote_plus(str(password))}@{host}:{self.PORT}/{self.DATABASE_NAME}"


class Logging(BaseSettings):
    LEVEL: logger.LoggerLevel = logger.LoggerLevel.DEBUG
    FOLDER_PATH: pathlib.Path = pathlib.Path("./logs")

    @field_validator("FOLDER_PATH")
    @classmethod
    def __create_dir_if_not_exist(
        cls,
        v: pathlib.Path,
    ):
        if not v.exists():
            v.mkdir(exist_ok=True, parents=True)
        return v


class APIServer(BaseSettings):
    HOST: str = "localhost"
    PORT: PositiveInt = 5000

    # --- SECURITY SETTINGS ---
    X_ACCESS_TOKEN: SecretStr = SecretStr("secret")


class Centrifugo(BaseSettings):
    HOST: str = "localhost"
    PORT: PositiveInt = 8001


class Settings(BaseSettings):
    INSTANCE_APP_NAME: str = "project_name"
    API: APIServer

    # --- REPOSITORIES ---
    POSTGRES: Postgresql

    # --- OTHER SETTINGS ---
    LOGGER: Logging

    model_config = SettingsConfigDict(
        env_file=find_dotenv(".env"),
        env_file_encoding="utf-8",
        arbitrary_types_allowed=True,
        case_sensitive=True,
        env_nested_delimiter="__"
    )


ai_crm_env = Settings()