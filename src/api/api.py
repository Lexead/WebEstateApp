from fastapi import APIRouter

from .auth import router as auth_router
from .notes import router as notes_router

router = APIRouter()
router.include_router(auth_router, tags=["auth"])
router.include_router(notes_router, tags=["notes"])
