"""
Main API entrypoint
"""

# Third party imports
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

# Local application imports
from .routes import group
from .routes import health
from .routes import base
from .routes import user
from .routes import auth

from src.config import settings

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.local_secret_key)
base.router.include_router(group.router)
base.router.include_router(health.router)
base.router.include_router(user.router)
app.include_router(base.router)
app.include_router(auth.router)
