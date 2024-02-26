from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NoteListSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    created_at: datetime


class NoteCreateSchema(BaseModel):
    title: str
    content: str


class NoteFilterSchema(BaseModel):
    title: str = None
    created_at: datetime = datetime.utcnow()
