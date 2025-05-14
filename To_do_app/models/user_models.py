from ..database.connection import Base
from sqlalchemy import Boolean
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from enum import Enum


class UserRoles(str, Enum):
    USER = "User"
    Admin = "Admin"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=True)
    role: Mapped[UserRoles] = mapped_column(
        SQLEnum(UserRoles), nullable=False, default="User")

    todos: Mapped[list["Todos"]] = relationship(back_populates="user")

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(
        timezone.utc), onupdate=datetime.now(timezone.utc))
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
