from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey, String


class Image(Base):
    __tablename__ = 'images'

    image_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)