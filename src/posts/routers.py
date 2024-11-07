from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence

from database import get_session
from users.models import User
from posts.models import Post
from posts.schemas import CreatePostSchema, ReadPostSchema
from posts.services import (
    create_post,
    read_post,
    update_post,
    delete_post,
    get_all_posts,
    get_posts_by_author,
    get_my_posts,
)
from security.services import get_current_user
from images.models import Image


router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=CreatePostSchema)
async def add_new_post(
    post: CreatePostSchema,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> ReadPostSchema:
    """
    создает новый пост
    user: текущий пользователь
    возвращает ReadPostSchema
    """
    new_post = await create_post(session=session, post=post, user=user)
    return ReadPostSchema(
        author=new_post.author_username,
        title=new_post.title,
        body=new_post.body,
        created_at=new_post.created_at,
    )


@router.get("/{slug}", response_model=ReadPostSchema)
async def get_one_post(
    slug: str,
    session: AsyncSession = Depends(get_session),
) -> ReadPostSchema:
    """
    получение поста по слагу
    возвращает ReadPostSchema
    """
    post = await read_post(session, slug)
    if post:
        query = select(Image.filename).where(Image.post_id == post.id)
        result = await session.execute(query)
        filenames = [f"/uploads/{row.filename}" for row in result]
        return ReadPostSchema(
            author=post.author_username,
            title=post.title,
            body=post.body,
            created_at=post.created_at,
            images=filenames,
        )
    else:
        raise HTTPException(status_code=404, detail="post not found")


@router.put("/{slug}", response_model=ReadPostSchema)
async def update_old_post(
    post_data: CreatePostSchema,
    slug: str,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> ReadPostSchema:
    """
    обновляет (изменяет значение полей) уже созданный пост
    если пост существует и пользователь, отправляющий запрос, является автором
    возвращает объект ReadPostSchema
    """
    old_post = await read_post(session, slug)
    if old_post:
        if old_post.author_username == user.username:
            updated_post = await update_post(
                session=session, slug=slug, post_data=post_data
            )
            return ReadPostSchema(
                author=updated_post.author_username,
                title=updated_post.title,
                body=updated_post.body,
                created_at=old_post.created_at,
                slug=updated_post.slug,
            )
        else:
            raise HTTPException(status_code=403, detail="forbidden")
    else:
        raise HTTPException(status_code=404, detail="post not found")


@router.delete("/{slug}")
async def post_delete(
    slug: str,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> str:
    """
    удаляет пост из базы данных
    user: текущий пользователь
    если пользователь не является автором - ошибка 403
    возвращает сообщение об успешном удалении
    """
    post = await read_post(session, slug)
    if post:
        if user == post.author_username:
            return await delete_post(session, slug)
        else:
            raise HTTPException(status_code=403, detail="forbidden")
    else:
        raise HTTPException(status_code=404, detail="post not found")


@router.get("/")
@cache(expire=60)
async def get_posts(session: AsyncSession = Depends(get_session)) -> Sequence[Post]:
    """
    получение всех постов всех авторов
    если постов нет - ошибка 404
    """
    try:
        return await get_all_posts(session)
    except:
        raise HTTPException(status_code=404, detail="no posts found")


@router.get("/{username}/posts")
async def get_authors_posts(
    author: str,
    session: AsyncSession = Depends(get_session),
):
    """
    возвращает посты конкретного автора
    """
    posts = await get_posts_by_author(session, author)
    if not posts:
        raise HTTPException(status_code=404, detail="no posts found")

    return posts


@router.get("/{username}/my_posts")
async def my_posts(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    возвращает посты текущего пользователя
    """
    posts = await get_my_posts(session=session, user=user)
    if not posts:
        raise HTTPException(status_code=404, detail="post not found")

    return posts
