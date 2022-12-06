from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from dataclasses import dataclass, fields
import jwt

# Local application imports
from src.config import settings


@dataclass
class OAuthUserInfo:
    email: str
    email_verified: bool
    exp: int
    given_name: str
    locale: str
    name: str
    picture: str
    sub: str


# OAuth settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_oauth_userinfo(token: str = Depends(oauth2_scheme)):
    try:
        decode = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=["HS256"],
            audience=settings.google_client_id,
        )
        field_names = [field.name for field in fields(OAuthUserInfo)]
        filtered = {k: decode[k] for k in field_names}
        return OAuthUserInfo(**filtered)
    except Exception:
        raise HTTPException(status_code=401, detail="Not Authorized")
