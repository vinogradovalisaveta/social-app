from typing import List

from sqlalchemy import ForeignKey, String, Text, func, DateTime, Integer, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_username: Mapped[str] = mapped_column(String, ForeignKey("users.username"))
    author: Mapped["User"] = relationship("User", back_populates="posts")
    title: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, index=True, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(256), nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=True)
    location: Mapped[str] = mapped_column(String, nullable=True)
    bio: Mapped[str] = mapped_column(String, nullable=True)

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


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subscriber_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    subscribed_to_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    subscriber: Mapped[List["User"]] = relationship(
        "User", foreign_keys=[subscriber_id], back_populates="subscriptions"
    )
    subscribed_to: Mapped[List["User"]] = relationship(
        "User", foreign_keys=[subscribed_to_id], back_populates="subscribers"
    )
