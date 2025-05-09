from ..database.connection import Base
from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date, datetime, timezone
from enum import Enum


class test_table(Base):
    __tablename__ = "testing"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


"""
class Todos:
    id int
    title str
    description str
    due_date str
    task_priority
"""


class Todos(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    due_date: Mapped[date] = mapped_column(nullable=True)
    task_priority: Mapped[TaskPriority] = mapped_column(
        SQLEnum(TaskPriority), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(
        timezone.utc), onupdate=datetime.now(timezone.utc))
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"<Todo {self.title} created at {self.created_at}>"
