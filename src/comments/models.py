from database import Base
from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("posts.id"), nullable=False
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
