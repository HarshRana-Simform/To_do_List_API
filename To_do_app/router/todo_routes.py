from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Body, Path, Query
from ..schemas.todo_schemas import TodoSchema, TodoUpdateSchema, TodoViewSchema
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..database.connection import get_db
from ..models.todo_models import Todos
from enum import Enum

# Endpoint	        Method	Description
# /todos	        Get	    Read all todo
# /create_todo      POST	Create a todo
# /todo/{todo_id}	GET	    Get a todo by id
# /todo/{todo_id}	PATCH	Update a todo by id
# /todo/{todo_id}	DELETE	Delete a todo by id

router = APIRouter()


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


@router.get("/todos/", response_model=list[TodoViewSchema], status_code=status.HTTP_200_OK)
def get_todos(db: Annotated[Session, Depends(get_db)], priority: Annotated[TaskPriority | None, Query(description="Filter by priority")] = None):

    stmt = select(Todos).where(Todos.deleted == False)

    if priority:
        stmt = stmt.where(Todos.task_priority == priority)

    todos = db.execute(stmt).scalars().all()
    if not todos:
        raise HTTPException(
            status_code=status.HTTP_200_OK, detail="You're all caught up on your tasks.")
    return todos


@router.post("/create_todo/", status_code=status.HTTP_201_CREATED)
def create_todo(todo: Annotated[TodoSchema, Body()], db: Annotated[Session, Depends(get_db)]):

    new_todo = Todos(
        title=todo.title,
        description=todo.description,
        due_date=todo.due_date,
        task_priority=todo.task_priority
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return {"success": "Todo created successfully!", "Added Data": new_todo}


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoViewSchema)
def get_todo(todo_id: Annotated[int, Path()], db: Annotated[Session, Depends(get_db)]):

    stmt = select(Todos).where(Todos.id == todo_id)

    todo = db.execute(stmt).scalars().first()
    if todo:
        return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="To-do not found.")


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: Annotated[int, Path()], db: Annotated[Session, Depends(get_db)]):

    stmt = select(Todos).where(Todos.id == todo_id)

    todo = db.execute(stmt).scalars().first()
    if todo:
        todo.deleted = True
        db.commit()
        db.refresh(todo)
        return {}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="To do not found.")


@router.patch("/todo/{todo_id}")
def update_todo(todo_id: Annotated[int, Path()], updated_todo: TodoUpdateSchema, db: Annotated[Session, Depends(get_db)]):

    stmt = select(Todos).where(Todos.id == todo_id)

    todo = db.execute(stmt).scalars().first()

    if todo:
        if updated_todo.title is not None:
            todo.title = updated_todo.title
        if updated_todo.description is not None:
            todo.description = updated_todo.description
        if updated_todo.due_date is not None:
            todo.due_date = updated_todo.due_date
        if updated_todo.task_priority is not None:
            todo.task_priority = updated_todo.task_priority

        db.commit()
        db.refresh(todo)

        return todo

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="To do not found.")
