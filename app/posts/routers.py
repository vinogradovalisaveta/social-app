from fastapi import APIRouter, Depends, HTTPException
from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.posts.schemas import CreatePostSchema, ReadPostSchema
from app.posts.services import (
    update_post,
    delete_post,
    get_all_posts,
    get_posts_by_author,
    get_my_posts,
    get_post_by_slug,
)
from app.security.services import get_current_user
from app.models import User, Post

post_router = APIRouter(prefix="/posts", tags=["posts"])


@post_router.post("/", response_model=CreatePostSchema)
async def create_post(
    post: CreatePostSchema,
    session: AsyncSession = Depends(get_session),
    author: User = Depends(get_current_user),
):
    new_post = Post(**post.dict())
    new_post.author_username = author.username
    new_post.slug = slugify(post.title)
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)
    return new_post


@post_router.get("/{slug}")
async def get_post(slug: str, session: AsyncSession = Depends(get_session)):
    return await get_post_by_slug(session, slug)


@post_router.put("/{slug}", response_model=ReadPostSchema)
async def update(
    post_data: CreatePostSchema,
    slug: str,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    post = await get_post_by_slug(session, slug)
    if post.author_id == user.id:
        updated_post = await update_post(
            session=session, slug=slug, post_data=post_data
        )
        return ReadPostSchema(
            author=updated_post.author_id,
            title=updated_post.title,
            body=updated_post.body,
            created_at=post.created_at,
            slug=updated_post.slug,
        )
    else:
        raise HTTPException(status_code=403, detail="forbidden")


@post_router.delete("/{slug}")
async def post_delete(
    slug: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    post_data = await get_post_by_slug(session, slug)
    if post_data is None:
        raise HTTPException(status_code=404, detail="post not found")
    if post_data.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="forbidden")

    try:
        await delete_post(session, slug)
    except:
        raise HTTPException(status_code=500, detail="unknown error")


@post_router.get("/")
async def get_posts(session: AsyncSession = Depends(get_session)):
    try:
        return await get_all_posts(session)
    except:
        raise HTTPException(status_code=404, detail="no posts found")


@post_router.get("/{username}/posts")
async def get_authors_posts(
    author: str,
    session: AsyncSession = Depends(get_session),
):
    posts = await get_posts_by_author(session, author)
    if not posts:
        raise HTTPException(status_code=404, detail="no posts found")

    return posts


@post_router.get("/{username}/my_posts")
async def my_posts(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    posts = await get_my_posts(session=session, user=user)
    if not posts:
        raise HTTPException(status_code=404, detail="post not found")

    return posts
