from fastapi import FastAPI

from app.users.routers import router

app = FastAPI()

app.include_router(router)
