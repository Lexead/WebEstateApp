from typing import Any

from fastapi import HTTPException, status


class BadRequestException(HTTPException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail if detail else "Bad request",
        )


class NotFoundException(HTTPException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail if detail else "Not found",
        )
