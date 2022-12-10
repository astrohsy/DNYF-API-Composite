"""
See:
- https://fastapi.tiangolo.com/advanced/settings/
- https://pydantic-docs.helpmanual.io/usage/settings/
"""

import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    jwt_secret_key: str
    google_client_id: str
    google_client_secret: str
    debug: bool

    class Config:
        env_file = ".env"


class ProdSettings(Settings):
    class Config:
        env_prefix = "PROD_"


class DevSettings(Settings):
    pass


if os.getenv("PROD_FLAG"):
    settings = ProdSettings()
else:
    settings = DevSettings()
