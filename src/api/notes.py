from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from ..core import BadRequestException, NotFoundException, decode_access_token
from ..db import get_session
from ..models import BlackListToken, Note, User
from ..schemas import NoteCreateSchema, NoteFilterSchema, NoteListSchema

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.get("/notes")
async def get_notes(
    token: Annotated[str, Depends(oauth2_scheme)],
    filter_data: NoteFilterSchema = None,
    session: AsyncSession = Depends(get_session),
):
    payload = decode_access_token(token)
    black_list_token = await BlackListToken.get_by_id(session, UUID(payload["jti"]).hex)
    if black_list_token:
        raise BadRequestException("Token is blacklisted")
    user = await User.get_by_id(session, UUID(payload["sub"]).hex)
    if not user:
        raise NotFoundException(detail="User not found")
    if not filter_data:
        notes = await Note.find_by_user(session, user)
    else:
        notes = await Note.filter(
            session,
            Note.title == filter_data.title,
            func.extract("day", Note.created_at) == filter_data.created_at.day,
            func.extract("year", Note.created_at) == filter_data.created_at.year,
            Note.user_id == user.id,
        )

    return [NoteListSchema.from_orm(note) for note in notes]


@router.post("/notes", status_code=201)
async def note_create(
    token: Annotated[str, Depends(oauth2_scheme)],
    data: NoteCreateSchema,
    session: AsyncSession = Depends(get_session),
):
    payload = decode_access_token(token)
    black_list_token = await BlackListToken.get_by_id(session, UUID(payload["jti"]).hex)
    if black_list_token:
        raise BadRequestException("Token is blacklisted")
    user = await User.get_by_id(session, UUID(payload["sub"]).hex)
    if not user:
        raise NotFoundException(detail="User not found")

    await Note.create(session, **data.model_dump(), user_id=user.id)

    return {"message": "Note successfully created"}


@router.patch("/notes/{id}")
async def note_update(
    token: Annotated[str, Depends(oauth2_scheme)],
    id: UUID,
    data: dict,
    session: AsyncSession = Depends(get_session),
):
    payload = decode_access_token(token)
    black_list_token = await BlackListToken.get_by_id(session, UUID(payload["jti"]).hex)
    if black_list_token:
        raise BadRequestException("Token is blacklisted")
    note = await Note.get_by_id(session, id)
    if not note:
        raise NotFoundException(detail="Note not found")

    await note.update_instance(session, **data)

    return {"message": "Note successfully updated"}


@router.delete("/notes/{id}")
async def note_delete(
    token: Annotated[str, Depends(oauth2_scheme)],
    id: UUID,
    session: AsyncSession = Depends(get_session),
):
    payload = decode_access_token(token)
    black_list_token = await BlackListToken.get_by_id(session, UUID(payload["jti"]).hex)
    if black_list_token:
        raise BadRequestException("Token is blacklisted")
    note = await Note.get_by_id(session, id)
    if not note:
        raise NotFoundException(detail="Note not found")

    await note.delete_instance(session)

    return {"message": "Note successfully updated"}
