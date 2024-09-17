from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from database import get_session
from posts.services import get_all_posts
from posts.services import read_post
from users.services import get_user_by_username
from posts.services import get_posts_by_author
from comments.services import get_comments_to_post
from likes.services import get_likes
from subscription.services import get_follows, get_followers

router = APIRouter(tags=["pages"])

templates = Jinja2Templates(directory="templates")


@router.get("/index")
async def get_index_page(
    request: Request, session: AsyncSession = Depends(get_session)
):
    posts = await get_all_posts(session)
    context = {"request": request, "posts": posts}
    return templates.TemplateResponse("index.html", context)


@router.get("/posts/{slug}")
async def get_post_detail_page(
    request: Request,
    username: str,
    slug: str,
    session: AsyncSession = Depends(get_session),
):
    post = await read_post(session, slug)
    comments = await get_comments_to_post(session, post.slug)
    likes = await get_likes(post.id, session)
    followers = await get_followers(user=username, session=session)
    context = {
        "request": request,
        "post": post,
        "comments": comments,
        "likes": likes,
        "followers": followers,
    }
    return templates.TemplateResponse("post_detail.html", context)


@router.get("/users/{username}")
async def get_profile_page(
    request: Request, username: str, session: AsyncSession = Depends(get_session)
):
    user = await get_user_by_username(session, username)
    posts = await get_posts_by_author(session, username)
    context = {"request": request, "user": user, "posts": posts}
    return templates.TemplateResponse("profile_page.html", context)
