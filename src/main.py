from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from images.routers import router as image_router
from posts.routers import router as post_router
from subscription.routers import router as subs_router
from users.routers import router as user_router
from comments.routers import router as comment_router
from likes.routers import router as like_router

app = FastAPI()


app.include_router(image_router)
app.include_router(comment_router)
app.include_router(subs_router)
app.include_router(post_router)
app.include_router(user_router)
app.include_router(like_router)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(
        "redis://localhost", encoding="utf8", decode_responces=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
