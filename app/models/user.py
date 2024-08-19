from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(256))
    password: Mapped[str] = mapped_column(String(256))

    # one-to-one with profile
    profile: Mapped["Profile"] = relationship(back_populates="user")


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=True)
    location: Mapped[str] = mapped_column(String(150), nullable=True)
    bio: Mapped[str] = mapped_column(String(150), nullable=True)

    # one-to-one with user
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="profile")
