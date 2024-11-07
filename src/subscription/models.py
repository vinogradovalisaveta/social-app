from typing import List
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


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
