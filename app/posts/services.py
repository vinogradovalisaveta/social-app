from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Post
from app.posts.schemas import CreatePostSchema
from app.security.services import get_current_user


async def create_post(
    session: AsyncSession,
    post: CreatePostSchema,
    user: User = Depends(get_current_user),
) -> Post:
    new_post = Post(**post.model_dump())
    new_post.author_id = user.id
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)
    return new_post


async def read_post():
    pass


async def update_post():
    pass


async def delete_post():
    pass
