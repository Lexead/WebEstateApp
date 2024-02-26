import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from fastapi import Response
from jwt import decode, encode
from passlib.hash import pbkdf2_sha256

from ..core import settings
from ..models import User
from ..schemas import JwtTokenSchema, TokenPair


def create_access_token(payload: dict, seconds: int | None = None) -> JwtTokenSchema:
    expire = datetime.utcnow() + timedelta(seconds=seconds or settings.dev_settings.ACCESS_TOKEN_EXPIRE)

    payload["exp"] = expire

    token = JwtTokenSchema(
        token=encode(payload, settings.dev_settings.JWT_SECRET_KEY, algorithm=settings.dev_settings.JWT_ALGORITHM),
        payload=payload,
        expire=expire,
    )

    return token


def create_refresh_token(payload: dict) -> JwtTokenSchema:
    expire = datetime.utcnow() + timedelta(seconds=settings.dev_settings.REFRESH_TOKEN_EXPIRE)

    payload["exp"] = expire

    token = JwtTokenSchema(
        token=encode(payload, settings.dev_settings.JWT_SECRET_KEY, algorithm=settings.dev_settings.JWT_ALGORITHM),
        expire=expire,
        payload=payload,
    )

    return token


def create_token_pair(user: User) -> TokenPair:
    payload = {"sub": str(user.id), "jti": str(uuid.uuid4()), "iat": datetime.utcnow()}

    return TokenPair(
        access_token=create_access_token(payload={**payload}),
        refresh_token=create_refresh_token(payload={**payload}),
    )


def decode_access_token(token: str) -> dict:
    return decode(token, settings.dev_settings.JWT_SECRET_KEY, algorithms=[settings.dev_settings.JWT_ALGORITHM])


def add_refresh_token_cookie(response: Response, token: str):
    exp = datetime.utcnow() + timedelta(seconds=settings.dev_settings.REFRESH_TOKEN_EXPIRE)
    exp.replace(tzinfo=timezone.utc)

    response.set_cookie(
        key="refresh",
        value=token,
        expires=int(exp.timestamp()),
        httponly=True,
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pbkdf2_sha256.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)
