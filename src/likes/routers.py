from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_session
from likes.models import Like
from likes.services import get_likes
from security.services import get_current_user
from users.models import User


router = APIRouter(tags=["likes"])


@router.post("/likes")
async def like_post(
    post_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    new_like = Like(user_id=user.id, post_id=post_id)
    session.add(new_like)
    await session.commit()
    await session.refresh(new_like)
    return new_like


@router.delete("/likes/{post.id}")
async def unlike_post(
    post_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    query = await session.execute(
        select(Like).where(Like.post_id == post_id, Like.user_id == user.id)
    )
    like = query.scalar()

    if like is None:
        raise HTTPException(status_code=404, detail="like not found")

    await session.delete(like)
    await session.commit()
    return like


@router.get("/posts/{post.id}/likes")
async def get_likes_to_post(post_id: int, session: AsyncSession = Depends(get_session)):
    likes = await get_likes(post_id, session)
    return likes
