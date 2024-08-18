from fastapi import FastAPI

from app.user import router

app = FastAPI()

app.include_router(router)
