# Local application imports


# Third party imports
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
import jwt

# Local application imports
from src.config import settings

# Scheme for the Authorization header
# OAuth settings
config_data = {
    "JWT_SECRET_KEY": settings.jwt_secret_key,
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

router = APIRouter(tags=["auth"])


def create_fake_user_jwt(email):
    fake_user_info = {
        "iss": "https://accounts.google.com",
        "azp": "250549377484-j9n0avvd8l096av7s3hn9ke59eg5j64a.apps.googleusercontent.com",
        "aud": "250549377484-j9n0avvd8l096av7s3hn9ke59eg5j64a.apps.googleusercontent.com",
        "email_verified": True,
        "at_hash": "a1P96VhO9HlXHqHZsdi-rQ",
        "nonce": "vpyI5IAmtEQIavL7o5XC",
        "name": "Joe",
        "picture": "https://lh3.googleusercontent.com/a/AEdFTp4UEzvKkqEN4KTERZhQMRFJMpdsrwRWuGf6geBn=s96-c",
        "given_name": "Joe",
        "locale": "ko",
        "iat": 1670697109,
    }
    fake_user_info["email"] = email
    fake_user_info["sub"] = "105340115531053206617"
    encoded_jwt = jwt.encode(fake_user_info, settings.jwt_secret_key, algorithm="HS256")
    return encoded_jwt


@router.get("/fake-auth/{email}")
async def fake_auth(email: str):
    if settings.debug:
        return {
            "access_token": create_fake_user_jwt(email),
            "token_type": "bearer",
            "debug": True,
        }
    else:
        return {}


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    if settings.debug:
        return RedirectResponse(url=redirect_uri)

    ret = await oauth.google.authorize_redirect(request, redirect_uri)
    return ret


@router.get("/auth")
async def auth(request: Request):
    if settings.debug:
        return {
            "access_token": create_fake_user_jwt("debug"),
            "token_type": "bearer",
            "debug": True,
        }
    access_token = await oauth.google.authorize_access_token(request)
    userinfo = access_token["userinfo"]
    encoded_jwt = jwt.encode(userinfo, settings.jwt_secret_key, algorithm="HS256")
    return {"access_token": encoded_jwt, "token_type": "bearer"}
