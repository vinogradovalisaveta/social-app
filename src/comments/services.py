from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from comments.models import Comment


async def get_comments_to_post(session: AsyncSession, post_slug: str):
    query = select(Comment).where(Comment.post_slug == post_slug)
    comments = (await session.execute(query)).scalars().all()
    return comments
