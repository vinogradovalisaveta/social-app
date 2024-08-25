from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.posts.schemas import CreatePostSchema, ReadPostSchema
from app.posts.services import create_post, read_post, update_post, delete_post
from app.security.services import get_current_user
from app.models import User

post_router = APIRouter(prefix="/posts", tags=["posts"])


@post_router.post("/", response_model=ReadPostSchema)
async def add_new_post(
    post: CreatePostSchema,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    new_post = await create_post(session=session, post=post, user=user)
    return ReadPostSchema(
        author=new_post.author_id,
        title=new_post.title,
        body=new_post.body,
        created_at=new_post.created_at,
        slug=new_post.slug,
    )


@post_router.get("/{slug}")
async def get_one_post(
    slug: str,
    session: AsyncSession = Depends(get_session),
):
    return await read_post(session, slug)


@post_router.put("/{slug}", response_model=ReadPostSchema)
async def update_old_post(
    post_data: CreatePostSchema,
    slug: str,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    old_post = await read_post(session, slug)
    if old_post.author_id == user.id:
        updated_post = await update_post(
            session=session, slug=slug, post_data=post_data
        )
        return ReadPostSchema(
            author=updated_post.author_id,
            title=updated_post.title,
            body=updated_post.body,
            created_at=old_post.created_at,
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
    post_data = await read_post(session, slug)
    if post_data is None:
        raise HTTPException(status_code=404, detail="post not found")
    if post_data.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="forbidden")

    try:
        await delete_post(session, slug)
    except:
        raise HTTPException(status_code=500, detail="unknown error")
