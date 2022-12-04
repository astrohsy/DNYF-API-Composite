# Local application imports


# Third party imports
from fastapi import APIRouter, Depends, Security, Request
from authlib.integrations.starlette_client import OAuth
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuthError
from starlette.config import Config

# Local application imports
from src.config import settings

# Scheme for the Authorization header
# OAuth settings
config_data = {
    "GOOGLE_CLIENT_ID": settings.google_client_id,
    "GOOGLE_CLIENT_SECRET": settings.google_client_secret,
}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

router = APIRouter(tags=["login"])


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    ret = await oauth.google.authorize_redirect(request, redirect_uri)
    return ret


@router.get("/auth")
async def auth(request: Request):
    access_token = await oauth.google.authorize_access_token(request)
    userinfo = access_token["userinfo"]
    email = userinfo["email"]
    print(email)
    request.session["userinfo"] = dict(userinfo)
    return RedirectResponse(url="/")
