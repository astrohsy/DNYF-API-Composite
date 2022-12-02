"""
Main API entrypoint
"""

# Third party imports
from fastapi import FastAPI

# Local application imports
from .routes import group
from .routes import health
from .routes import base
from .routes import user

app = FastAPI()
base.router.include_router(group.router)
base.router.include_router(health.router)
base.router.include_router(user.router)
app.include_router(base.router)
