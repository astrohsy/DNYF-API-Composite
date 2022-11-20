"""
Main API entrypoint
"""
# Standard library imports
import json

# Third party imports
from fastapi import FastAPI, Request
from starlette.responses import StreamingResponse
from starlette.concurrency import iterate_in_threadpool
import boto3

# Local application imports
from .routes import group
from .routes import health
from .routes import base
from src.config import settings

app = FastAPI()
base.router.include_router(group.router)
base.router.include_router(health.router)
app.include_router(base.router)
