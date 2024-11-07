from datetime import datetime

from pydantic import BaseModel
from typing import List


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

    pass


class ReadPostSchema(BasePostModel):
    """
    модель для отображения поста, наследуется от BasePostModel и содержит
    дополнительные поля author и created_at
    """

    author: str
    created_at: datetime
    images: List[str] = []
