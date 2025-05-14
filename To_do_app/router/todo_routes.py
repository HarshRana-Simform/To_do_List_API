from typing import Annotated
from fastapi import APIRouter, Depends, status, Body, Path, Query
from ..schemas.todo_schemas import TodoSchema, TodoUpdateSchema, TaskPriority
from ..schemas.relationship_schemas import TodoViewRelSchema
from sqlalchemy.orm import Session
from ..database.connection import get_db
from ..handlers import todo_handler
from ..core.authentication import verify_token

# Endpoint	        Method	Description
# /todos	        Get	    Read all todo
# /create_todo      POST	Create a todo
# /todo/{todo_id}	GET	    Get a todo by id
# /todo/{todo_id}	PATCH	Update a todo by id
# /todo/{todo_id}	DELETE	Delete a todo by id

router = APIRouter()


@router.get("/todos/", response_model=list[TodoViewRelSchema], status_code=status.HTTP_200_OK)
def get_todos(db: Annotated[Session, Depends(get_db)], priority: Annotated[TaskPriority | None, Query(description="Filter by priority")] = None):
    return todo_handler.get_all(db, priority)


@router.post("/create_todo/", status_code=status.HTTP_201_CREATED)
def create_todo(todo: Annotated[TodoSchema, Body()], db: Annotated[Session, Depends(get_db)], user_id: Annotated[int, Depends(verify_token)]):
    return todo_handler.create(todo, db, user_id)


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoViewRelSchema)
def get_todo(todo_id: Annotated[int, Path()], db: Annotated[Session, Depends(get_db)]):
    return todo_handler.get_one(todo_id, db)


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: Annotated[int, Path()], db: Annotated[Session, Depends(get_db)]):
    return todo_handler.delete(todo_id, db)


@router.patch("/todo/{todo_id}")
def update_todo(todo_id: Annotated[int, Path()], updated_todo: TodoUpdateSchema, db: Annotated[Session, Depends(get_db)]):
    return todo_handler.patch_update(todo_id, updated_todo, db)
