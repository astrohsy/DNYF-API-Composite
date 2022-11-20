"""
Main API entrypoint
"""

# Third party imports
from fastapi import FastAPI
from starlette.concurrency import iterate_in_threadpool

# Local application imports
from .routes import group
from .routes import health
from .routes import base

app = FastAPI()
base.router.include_router(group.router)
base.router.include_router(health.router)
app.include_router(base.router)
