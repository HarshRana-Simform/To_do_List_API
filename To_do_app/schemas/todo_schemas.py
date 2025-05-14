from datetime import date
from pydantic import BaseModel, Field, field_validator, AfterValidator
from typing import Annotated, Optional
from enum import Enum


def check_due_date(value: date):

    if value and value < date.today():
        raise ValueError('Date must be today or in the future')
    return value


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TodoSchema(BaseModel):
    title: str = Field(description="The title of the task.", max_length=200)
    description: str | None = Field(
        default=None, description="Details of the task", max_length=500)
    due_date: Annotated[date | None, AfterValidator(check_due_date)] = Field(default=None,
                                                                             description="The deadline you want to set for the task.")
    task_priority: TaskPriority


class TodoUpdateSchema(BaseModel):

    title: str | None = Field(default=None,
                              description="The title of the task.", max_length=200)
    description: str | None = Field(
        default=None, description="Details of the task", max_length=500)
    due_date: Annotated[date | None, AfterValidator(check_due_date)] = Field(default=None,
                                                                             description="The deadline you want to set for the task.")
    task_priority: TaskPriority | None = Field(default=None)

    # class Config:
    #     orm_mode = True


class TodoViewSchema(BaseModel):

    id: int
    title: str
    description: str | None
    due_date: date | None
    task_priority: TaskPriority

    class Config:
        from_attributes = True
