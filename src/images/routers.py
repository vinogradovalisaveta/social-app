import asyncio
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_session
from images.models import Image
from images.services import get_post_images
from posts.models import Post


image_router = APIRouter(tags=["images"])


# @image_router.post("/{post.slug}/images")
# async def add_images(
#     post_id: int,
#     files: List[UploadFile] = File(...),
#     session: AsyncSession = Depends(get_session),
# ):
#     """
#     на странице есть форма для загрузки изображений, после того, как мы выберем
#     изображения и подтвердим выбор, приложение создаст список задач (дать имена
#     всем файлам и указать путь сохранения на сервере) и asyncio.gather запустит
#     их одновременно и вернет список имен файлов
#     затем каждому файлу из списка будет назначен айди поста, который передан в
#     аргументах функции, сохранит в базу и вернет json, содержащий название
#     файлов и путь к ним
#     """
#     post = (
#         await session.execute(select(Post).where(Post.id == post_id))
#     ).scalar_one_or_none()
#     if not post:
#         raise HTTPException(status_code=404, detail="post not found")
#
#     tasks = [save_image(file) for file in files]
#     filenames = await asyncio.gather(*tasks)
#
#     images = []
#     for filename in filenames:
#         image = Image(post_id=post_id, filename=filename)
#         session.add(image)
#         images.append(image)
#
#     await session.commit()
#
#     for image in images:
#         await session.refresh(image)
#
#     return {
#         "images": [
#             {
#                 "filename": image.filename,
#                 "url": f"/uploads/{image.filename}",
#             }
#             for image in images
#         ]
#     }


@image_router.get("/{filename}")
async def get_image(filename: str, session: AsyncSession = Depends(get_session)):
    return FileResponse(f"uploads/{filename}", media_type="image/jpeg")


# @image_router.get("/{post.slug}/images")
# async def post_images_route(post_id: int, session: AsyncSession = Depends(get_session)):
#     post = (
#         await session.execute(select(Post).where(Post.id == post_id))
#     ).scalar_one_or_none()
#
#     if not post:
#         raise HTTPException(status_code=404, detail="post not found")
#
#     image_data = await get_post_images(post_id, session)
#
#     responses = []
#     for data in image_data:
#         responses.append({"data": data, "content_type": "image/jpeg"})
#
#     return responses
