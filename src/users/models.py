from typing import List
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from subscription.models import Subscription
from comments.models import Comment


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=True, default="none")
    location: Mapped[str] = mapped_column(String, nullable=True, default="none")
    bio: Mapped[str] = mapped_column(String, nullable=True, default="none")

    posts: Mapped[List["Post"]] = relationship("Post", back_populates="author")

    # relationship with subscription
    subscriptions: Mapped[List["Subscription"]] = relationship(
        "Subscription",
        foreign_keys="[Subscription.subscriber_id]",
        back_populates="subscriber",
    )
    subscribers: Mapped[List["Subscription"]] = relationship(
        "Subscription",
        foreign_keys="[Subscription.subscribed_to_id]",
        back_populates="subscribed_to",
    )

    comments: Mapped[list["Comment"]] = relationship(
        "Comment", backref="author", cascade="all, delete-orphan"
    )
