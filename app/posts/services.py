from fastapi import Depends
from slugify import slugify
from sqlalchemy import select, desc
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
    new_post.author_username = user.username
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

    if old_post.title != post_data.title:
        old_post.slug = slugify(post_data.title)

    old_post.title = post_data.title
    old_post.body = post_data.body

    session.add(old_post)
    await session.commit()
    await session.refresh(old_post)
    return old_post


async def delete_post(session: AsyncSession, slug: str):
    db_post = await read_post(session, slug)
    await session.delete(db_post)
    await session.commit()
    return {"message": "the post was successfully deleted"}


async def get_all_posts(session: AsyncSession):
    posts = await session.execute(select(Post).order_by(desc(Post.created_at)))
    posts = posts.scalars().all()
    return posts


async def get_posts_by_author(session: AsyncSession, author: str):
    posts = await session.execute(select(Post).where(Post.author_username == author))
    return posts.scalars().all()


async def get_my_posts(session: AsyncSession, user: User):

    posts = await session.execute(
        select(Post).where(Post.author_username == user.username)
    )
    posts = posts.scalars().all()

    return posts
