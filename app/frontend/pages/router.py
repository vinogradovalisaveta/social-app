from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates

from app.database import get_session
from app.posts.routers import get_post_by_slug
from app.posts.services import get_all_posts
from app.users.services import get_user_by_username

router = APIRouter(prefix="/pages", tags=["pages"])

templates = Jinja2Templates(directory="app/frontend/templates")


@router.get("/index")
async def get_post_list(request: Request, session: AsyncSession = Depends(get_session)):
    posts = await get_all_posts(session)
    return templates.TemplateResponse(
        "index.html", {"request": request, "posts": posts}
    )


@router.get("/profile/{username}")
async def get_profile(
    request: Request, username: str, session: AsyncSession = Depends(get_session)
):
    user = await get_user_by_username(username=username, session=session)
    return templates.TemplateResponse(
        "profile.html", {"request": request, "user": user}
    )


@router.get("/posts/{slug}", name="read_more")
async def read_more(
    request: Request, slug: str, session: AsyncSession = Depends(get_session)
):
    post = await get_post_by_slug(session, slug)
    return templates.TemplateResponse("post.html", {"request": request, "post": post})
