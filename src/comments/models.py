from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    post_slug: Mapped[str] = mapped_column(
        String, ForeignKey("posts.slug"), nullable=False
    )
    parent_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("comments.id"), nullable=True
    )
    author_username: Mapped[str] = mapped_column(
        String, ForeignKey("users.username"), nullable=False
    )
    text: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    replies = relationship(
        "Comment",
        backref="parent",
        cascade="all, delete-orphan",
        remote_side=[id],
        single_parent=True,
    )
