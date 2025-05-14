from .todo_schemas import TodoViewSchema
from .user_schemas import ShowUserSchema


class TodoViewRelSchema(TodoViewSchema):
    user: ShowUserSchema


class ShowUserRelSchema(ShowUserSchema):
    todos: list[TodoViewSchema]
