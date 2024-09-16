from fastapi import Depends, UploadFile, Form, File
from slugify import slugify
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, List
from posts.models import Post
from users.models import User
from posts.schemas import CreatePostSchema
from security.services import get_current_user
import os
import uuid
import aiofiles
import asyncio

from images.models import Image


async def create_post(
    session: AsyncSession,
    post: CreatePostSchema,
    user: User = Depends(get_current_user),
    images: List[UploadFile] = File(...),
) -> Post:
    """
    Создает новый пост в базе данных
    session: объект для взаимодействия с базой данных
    post: данные для создания поста, переданные через CreatePostSchema
    user: функция для получения авторизированного пользователя, который
    добавляет новый пост
    возвращает объект класса Post
    """
    new_post = Post(**post.dict())
    new_post.author_username = user.username
    new_post.slug = slugify(post.title)
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)

    for image_url in post.images:
        db_image = Image(url=image_url)
        new_post.images.append(db_image)

    # for image in images:
    #     filename = f"{uuid.uuid4().hex}_{image.filename}"
    #
    #     # 'uploads' - folder for saving images
    #     filepath = os.path.join("uploads", filename)
    #
    #     # wb - write binary - запись в двоичном режиме
    #     async with aiofiles.open(filepath, "wb") as f:
    #         content = await image.read()
    #         await f.write(content)
    #
    #     new_image = Image(filename=filename, post_id=new_post.id)
    #     session.add(new_image)

    await session.commit()
    await session.refresh(new_post)

    return new_post


async def read_post(session: AsyncSession, slug: str) -> Post | None:
    """
    получение поста по слагу
    возвращает объект класса Post либо None (если пост не найден)
    """
    query = select(Post).where(Post.slug == slug)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def update_post(
    session: AsyncSession, slug: str, post_data: CreatePostSchema
) -> Post:
    """
    обновление поста по слагу
    если меняется заголовок поста, слаг тоже меняется
    возвращает объект класса Post
    """
    old_post = await read_post(session, slug)

    if old_post.title != post_data.title:
        old_post.slug = slugify(post_data.title)

    old_post.title = post_data.title
    old_post.body = post_data.body

    session.add(old_post)
    await session.commit()
    await session.refresh(old_post)
    return old_post


async def delete_post(session: AsyncSession, slug: str) -> str:
    """
    удаляет пост, возращает сообщение об успешном удалении
    """
    db_post = await read_post(session, slug)
    await session.delete(db_post)
    await session.commit()
    return "the post was successfully deleted"


async def get_all_posts(session: AsyncSession) -> Sequence[Post]:
    """
    получение всех постов из базы данных
    возвращает список всех постов
    """
    posts = await session.execute(select(Post).order_by(desc(Post.created_at)))
    posts = posts.scalars().all()
    return posts


async def get_posts_by_author(session: AsyncSession, author: str) -> Sequence[Post]:
    """
    получение постов конкретного автора
    возвращает список всех постов автора
    """
    posts = await session.execute(select(Post).where(Post.author_username == author))
    return posts.scalars().all()


async def get_my_posts(session: AsyncSession, user: User) -> Sequence[Post]:
    """
    получение постов аутентифицированного пользователя
    возвращает список постов
    """
    posts = await session.execute(
        select(Post).where(Post.author_username == user.username)
    )
    return posts.scalars().all()
