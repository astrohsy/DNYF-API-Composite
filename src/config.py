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
    auth0_client_id: str
    auth0_public_key: str
    debug: bool

    class Config:
        env_file = ".env"


class ProdSettings(Settings):
    group_microservice_url = "TBD"
    users_microservice_url = "TBD"
    contacts_microservice_url = "TBD"

    class Config:
        env_prefix = "PROD_"


class DevSettings(Settings):
    group_microservice_url = "http://dnyf-groups-microservice:8101"
    users_microservice_url = "http://dnyf-users-microservice:4103"
    contacts_microservice_url = "http://dnyf-contacts-microservice:5005"


if os.getenv("PROD_FLAG"):
    settings = ProdSettings()
else:
    settings = DevSettings()
