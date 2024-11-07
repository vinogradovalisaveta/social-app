import os

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from .models import Image


async def save_image(file: UploadFile) -> str:
    # generation of unique filename
    filename = f"{uuid.uuid4().hex}_{file.filename}"

    # 'uploads' - folder for saving images
    filepath = os.path.join("uploads", filename)

    return filepath


async def get_post_images(post_id: int, session: AsyncSession):
    # getting images from the database
    images = await session.execute(select(Image).where(Image.post_id == post_id))

    return images.scalars().all()
