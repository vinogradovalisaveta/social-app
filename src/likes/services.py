from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from likes.models import Like


async def get_likes(post_id: int, session: AsyncSession = Depends()):
    query = select(Like).where(Like.post_id == post_id)
    likes = await session.execute(query)
    return likes.scalars().all()
