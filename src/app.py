"""
Main API entrypoint
"""

# Third party imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

# Local application imports
from .routes import group
from .routes import health
from .routes import base
from .routes import user
from .routes import auth

from src.config import settings

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.jwt_secret_key)
base.router.include_router(group.router)
base.router.include_router(health.router)
base.router.include_router(user.router)
app.include_router(base.router)
app.include_router(auth.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
