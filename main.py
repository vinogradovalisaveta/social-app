from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.frontend.pages.router import router
from app.posts.routers import post_router
from app.subscription.routers import subs_router
from app.users.routers import user_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/frontend/static"), name="static")

app.include_router(router)
app.include_router(subs_router)
app.include_router(post_router)
app.include_router(user_router)
