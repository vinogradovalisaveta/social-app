import logging

from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.database import get_session
from app.models import User
from app.posts.routers import get_post_by_slug
from app.posts.services import get_all_posts, get_posts_by_author
from app.security.services import authenticate_user, get_current_user
from app.security.token import create_jwt_token_pair
from app.users.services import get_user_by_username

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/pages", tags=["pages"])

templates = Jinja2Templates(directory="app/frontend/templates")


@router.get("/index")
async def get_post_list(request: Request, session: AsyncSession = Depends(get_session)):
    posts = await get_all_posts(session)
    return templates.TemplateResponse(
        "index.html", {"request": request, "posts": posts}
    )


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse(
        "base.html", {"request": request, "user": current_user}
    )


@router.get("/profile/{username}")
async def get_profile(
    request: Request, username: str, session: AsyncSession = Depends(get_session)
):
    user = await get_user_by_username(username=username, session=session)

    if user is None:
        raise HTTPException(status_code=404, detail="user not found")

    posts = await get_posts_by_author(session=session, author=user.username)

    return templates.TemplateResponse(
        "profile.html", {"request": request, "user": user, "posts": posts}
    )


@router.get("/posts/{slug}", name="read_more")
async def read_more(
    request: Request, slug: str, session: AsyncSession = Depends(get_session)
):
    post = await get_post_by_slug(session, slug)
    return templates.TemplateResponse("post.html", {"request": request, "post": post})


@router.get("/login", response_class=HTMLResponse)
async def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
async def login_user(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(session, form_data.username, form_data.password)

    token_pair = await create_jwt_token_pair(user_username=user.username)

    return RedirectResponse(url="/pages/index", status_code=303)
