from fastapi import APIRouter, Request, Depends, HTTPException, Form, Body, Response
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


from database import get_session
from posts.services import get_all_posts, get_posts_by_author, read_post
from users.models import User
from users.services import get_user_by_username

from security.services import get_current_user

from posts.schemas import CreatePostSchema
from posts.services import create_post

from users.routers import authenticate
from users.schemas import LoginSchema

from security.token import create_jwt_token

router = APIRouter(prefix="/pages", tags=["pages"])

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_index_page(
    request: Request, session: AsyncSession = Depends(get_session)
):
    posts = await get_all_posts(session)
    context = {"request": request, "posts": posts}
    return templates.TemplateResponse("index.html", context)


@router.get("/users/{username}")
async def get_user_profile_page(
    request: Request, username: str, session: AsyncSession = Depends(get_session)
):
    user = await get_user_by_username(session, username)
    posts = await get_posts_by_author(session, username)
    context = {"request": request, "user": user, "posts": posts}
    return templates.TemplateResponse("user_profile.html", context)


@router.get("/posts/{slug}")
async def get_post_detail_page(
    request: Request, slug: str, session: AsyncSession = Depends(get_session)
):
    post = await read_post(session, slug)
    # post_images = post.images
    if not post:
        raise HTTPException(status_code=404, detail="post not found")

    context = {"request": request, "post": post}
    return templates.TemplateResponse("post_detail.html", context)


@router.get("/add-new-post")
async def get_add_new_post(request: Request):
    return templates.TemplateResponse("add_new_post.html", {"request": request})


@router.post("/add-new-post")
async def post_add_new_post(
    request: Request,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    title: str = Form(...),
    body: str = Form(...),
    images: List[str] = Form(...),
):
    uploaded_images = []
    for image_name in images:
        for image in request.form.getlist("images[]"):
            if image_name == image.filename:
                uploaded_images.append(image)
                break

    new_post = await create_post(
        session=session,
        post=CreatePostSchema(author=user.username, title=title, body=body),
        images=uploaded_images,
    )

    return new_post


@router.get("/login")
async def get_login_page(request: Request):
    return templates.TemplateResponse("login_page.html", {"request": request})


@router.post("/login")
async def post_login_page(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await authenticate(
        session=session, form_data=form_data
    )  # current_user = await get_current_user(session)
    # return RedirectResponse('/')
    return templates.TemplateResponse(
        "index.html", {"request": request, "current_user": user}
    )


#

# router.get('/images/{filename}')
# async def get_image(filename: str, session: AsyncSession = Depends(get_session)):
#     return FileResponse(f'uploads/{filename}', media_type='image/jpeg')
