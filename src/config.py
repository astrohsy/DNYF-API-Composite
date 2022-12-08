"""
See:
- https://fastapi.tiangolo.com/advanced/settings/
- https://pydantic-docs.helpmanual.io/usage/settings/
"""

import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"


class ProdSettings(Settings):
    group_microservice_url = "TBD"

    class Config:
        env_prefix = "PROD_"


class DevSettings(Settings):
    group_microservice_url = "http://dnyf-groups-microservice:8101"


if os.getenv("PROD_FLAG"):
    settings = ProdSettings()
else:
    settings = DevSettings()
