from fastapi import FastAPI

from app.posts.routers import post_router
from app.subscription.routers import subs_router
from app.users.routers import user_router

app = FastAPI()

app.include_router(subs_router)
app.include_router(post_router)
app.include_router(user_router)
