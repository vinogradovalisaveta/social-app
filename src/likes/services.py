from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy import select
from likes.models import Like


async def get_likes(post_id: int, session: AsyncSession = Depends()):
    query = await session.execute(select(Like).where(Like.post_id == post_id))
    likes = query.scalars().all()
    return likes
