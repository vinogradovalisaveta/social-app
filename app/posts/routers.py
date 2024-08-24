from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.posts.schemas import CreatePostSchema
from app.posts.services import create_post
from app.security.services import get_current_user
from app.models import User

post_router = APIRouter(prefix='/posts', tags=['posts'])


@post_router.post('/', response_model=CreatePostSchema)
async def add_new_post(
        post: CreatePostSchema,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(get_current_user)
):
    return await create_post(session=session, post=post, user=user)