from datetime import datetime
from pydantic import BaseModel
from typing import List
from fastapi import Form, UploadFile
from images.schemas import Image


class BasePostModel(BaseModel):
    """
    базовая модель поста для валидации данных
    """

    title: str
    body: str


class CreatePostSchema(BasePostModel):
    """
    модель для создания поста, наследуется от BasePostModel
    """

    images: List[str]


class ReadPostSchema(BasePostModel):
    """
    модель для отображения поста, наследуется от BasePostModel и содержит
    дополнительные поля author и created_at
    """

    author: str
    created_at: datetime
    images: List[Image] = []
