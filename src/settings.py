from pydantic import BaseSettings


class AppSettings(BaseSettings):
    secret_key: str
