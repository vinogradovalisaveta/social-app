from fastapi import FastAPI

from app.posts.routers import post_router
from app.users.routers import router

app = FastAPI()

app.include_router(router)
app.include_router(post_router)
