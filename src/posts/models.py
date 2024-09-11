from sqlalchemy import Integer, String, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from users.models import User


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_username: Mapped[str] = mapped_column(String, ForeignKey("users.username"))
    author: Mapped["User"] = relationship("User", back_populates="posts")
    title: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, index=True, nullable=False, unique=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    comments: Mapped[list["Comment"]] = relationship(
        "Comment", backref="post", cascade="all, delete-orphan"
    )

    images: Mapped[list['Image']] = relationship(
        'Image', backref='post', cascade='all, delete-orphan'
    )
