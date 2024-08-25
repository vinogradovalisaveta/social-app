from fastapi import Depends
from slugify import slugify
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Post
from app.posts.schemas import CreatePostSchema
from app.security.services import get_current_user


async def create_post(
    session: AsyncSession,
    post: CreatePostSchema,
    user: User = Depends(get_current_user),
) -> Post:
    new_post = Post(**post.dict())
    new_post.author_id = user.id
    new_post.slug = slugify(post.title)
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)
    return new_post


async def read_post(session: AsyncSession, slug: str):
    query = select(Post).where(Post.slug == slug)
    result = await session.execute(query)
    return result.scalar()


async def update_post(session: AsyncSession, slug: str, post_data: CreatePostSchema):
    old_post = await read_post(session, slug)
    old_post.title = post_data.title
    old_post.body = post_data.body

    if old_post.title != post_data.title:
        old_post.slug = slugify(post_data.title)

    session.add(old_post)
    await session.commit()
    await session.refresh(old_post)
    return old_post


async def delete_post(session: AsyncSession, slug: str):
    db_post = await read_post(session, slug)
    await session.delete(db_post)
    await session.commit()
    return {"message": "the post was successfully deleted"}
