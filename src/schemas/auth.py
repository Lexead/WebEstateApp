from datetime import datetime

from pydantic import BaseModel, EmailStr


class LoginPayload(BaseModel):
    email: EmailStr
    password: str


class RegisterPayload(BaseModel):
    username: str
    email: EmailStr
    password: str


class JwtTokenSchema(BaseModel):
    token: str
    payload: dict
    expire: datetime


class TokenPair(BaseModel):
    access_token: JwtTokenSchema
    refresh_token: JwtTokenSchema
