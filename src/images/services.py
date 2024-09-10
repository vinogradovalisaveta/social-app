import os
import uuid

import aiofiles
import asyncio
from fastapi import UploadFile

from images.models import Image
from posts.models import Post
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def save_image(file: UploadFile) -> str:
    # generation of unique filename
    filename = f'{uuid.uuid4().hex}_{file.filename}'

    # 'uploads' - folder for saving images
    filepath = os.path.join('uploads', filename)

    # wb - write binary - запись в двоичном режиме
    async with aiofiles.open(filepath, 'wb') as f:
        content = await file.read()
        await f.write(content)

    return filename


async def read_image(filename: str) -> bytes:
    """
    asyncronous file reading

    rb - read binary - reading in binary mode
    """
    async with aiofiles.open(filename, 'rb') as f:
        return await f.read()


async def get_post_images(post_id: int, session: AsyncSession):
    # getting images from the database
    images = (await session.execute(
        select(Image).where(Image.post_id == post_id)
    )).scalars().all()

    # creating a list of asynchronous tasks
    tasks = [read_image(f'uploads/{image.filename}') for image in images]

    # asyncio.gather runs all the tasks in parallel
    image_data = await asyncio.gather(*tasks)
    return image_data
