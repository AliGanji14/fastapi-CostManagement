from collections.abc import Callable
from fastapi import Depends, HTTPException, Request, status
from users.models import UserModel
from core.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from core.config import settings
from core.i18n import get_translator

ACCESS_TOKEN_COOKIE_NAME = "access_token"
REFRESH_TOKEN_COOKIE_NAME = "refresh_token"
ALGORITHM = "HS256"


def create_token(user_id: int, token_type: str, expires_in: int):
    now = datetime.now(timezone.utc)
    payload = {
        "type": token_type,
        "user_id": user_id,
        "iat": now,
        "exp": now + timedelta(seconds=expires_in),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str, token_type: str, _: Callable[[str], str]):
    try:
        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = decoded.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=_("authentication failed, user_id not found in the payload"),
            )
        if decoded.get("type") != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=_("authentication failed, token type not valid"),
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=_("authentication failed, token is expired or invalid"),
        )


def get_authenticate_user(
    request: Request,
    db: Session = Depends(get_db),
    _: Callable[[str], str] = Depends(get_translator),
):
    token = request.cookies.get(ACCESS_TOKEN_COOKIE_NAME)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=_("authentication failed, access token cookie not found"),
        )

    user_id = decode_token(token, "access", _)
    user_obj = db.query(UserModel).filter_by(id=user_id).one_or_none()
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=_("authentication failed, user not found"),
        )
    return user_obj


def generate_access_token(
    user_id: int, expires_in: int = settings.ACCESS_TOKEN_EXPIRE_SECONDS
):
    return create_token(user_id, "access", expires_in)


def generate_refresh_token(
    user_id: int, expires_in: int = settings.REFRESH_TOKEN_EXPIRE_SECONDS
):
    return create_token(user_id, "refresh", expires_in)


def generate_regresh_token(
    user_id: int, expires_in: int = settings.REFRESH_TOKEN_EXPIRE_SECONDS
):
    return generate_refresh_token(user_id, expires_in)


def decode_refresh_token(token: str, _: Callable[[str], str]):
    return decode_token(token, "refresh", _)
