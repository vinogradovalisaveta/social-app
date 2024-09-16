from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.staticfiles import StaticFiles
from redis import asyncio as aioredis

from images.routers import image_router
from posts.routers import post_router
from subscription.routers import subs_router
from users.routers import user_router
from comments.routers import router
from pages.routers import router as page_router
from security.token import SECRET_KEY

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(page_router)
app.include_router(image_router)
app.include_router(router)
app.include_router(subs_router)
app.include_router(post_router)
app.include_router(user_router)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(
        "redis://localhost", encoding="utf8", decode_responces=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
