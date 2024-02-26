import uvicorn
from fastapi import FastAPI

from src.api import router

app = FastAPI()

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, port=8000, log_level="debug")
