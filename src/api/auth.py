from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Response
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..core import (
    BadRequestException,
    NotFoundException,
    add_refresh_token_cookie,
    create_access_token,
    create_token_pair,
    decode_access_token,
)
from ..db import get_session
from ..models import BlackListToken, User
from ..schemas import LoginPayload, RegisterPayload

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/register")
async def register(
    data: RegisterPayload,
    session: AsyncSession = Depends(get_session),
):
    user = await User.find_by_email(session, data.email)
    if user:
        raise BadRequestException(detail="Email has already registered")
    user = await User.find_by_username(session, data.username)
    if user:
        raise BadRequestException(detail="Username has already registered")

    await User.create(session, data.username, data.email, data.password)

    return {"message": "User registered successfully"}


@router.post("/login")
async def login(
    data: LoginPayload,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    user = await User.authenticate(
        session,
        data.email,
        data.password,
    )

    if not user:
        raise BadRequestException(detail="Incorrect email or password")

    token_pair = create_token_pair(user)

    add_refresh_token_cookie(response, token_pair.refresh_token)

    return {"data": token_pair.access_token, "message": "User logged in successfully"}


@router.post("/refresh")
async def refresh(refresh_token: Annotated[str | None, Cookie()] = None):
    if not refresh_token:
        raise BadRequestException(detail="refresh token required")
    payload = decode_access_token(refresh_token)
    return {"token": create_access_token(payload).token}


@router.get("/verify")
async def verify(token: str, session: AsyncSession = Depends(get_session)):
    payload = decode_access_token(token)
    black_list_token = await BlackListToken.get_by_id(session, payload["jti"])
    if black_list_token:
        raise BadRequestException("Token is blacklisted")
    user = await User.find_by_id(session, payload["sub"])
    if not user:
        raise NotFoundException(detail="User not found")

    return {"message": "Successfully verified"}


@router.post("/logout")
async def logout(token: Annotated[str, Depends(oauth2_scheme)] = None, session: AsyncSession = Depends(get_session)):
    payload = decode_access_token(token)
    black_list_token = await BlackListToken.get_by_id(session, payload["jti"])
    if black_list_token:
        raise BadRequestException("Token is blacklisted")
    await BlackListToken.create(session, id=payload["jti"], expire=datetime.utcfromtimestamp(payload["exp"]))
    return {"message": "Succesfully logout"}
