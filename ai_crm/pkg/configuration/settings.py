import pathlib
import typing
import urllib.parse

from pydantic import Field, field_validator, model_validator
from pydantic.types import PositiveInt, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv

from ai_crm.pkg.models import logger

class Postgresql(BaseSettings):
    HOST: str = "localhost"
    PORT: PositiveInt = 5432
    USER: str = "postgres"
    PASSWORD: SecretStr = SecretStr("postgres")
    DATABASE_NAME: str = "postgres"

    MIN_CONNECTION: PositiveInt = 1
    MAX_CONNECTION: PositiveInt = 16

    DSN: typing.Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def build_dsn(cls, values: dict):
        if isinstance(values, dict):
            password = values.get('PASSWORD', '')
            if hasattr(password, 'get_secret_value'):
                password = password.get_secret_value()
            
            # Строим DSN вручную для совместимости
            user = values.get('USER', 'postgres')
            host = values.get('HOST', 'localhost')
            port = values.get('PORT', 5432)
            db_name = values.get('DATABASE_NAME', 'postgres')
            
            values["DSN"] = f"postgresql://{user}:{urllib.parse.quote_plus(str(password))}@{host}:{port}/{db_name}"
        return values


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