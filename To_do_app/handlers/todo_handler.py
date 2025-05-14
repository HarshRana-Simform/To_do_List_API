from sqlalchemy.orm import Session
from sqlalchemy import select
from ..models.todo_models import Todos
from ..schemas.todo_schemas import TaskPriority, TodoSchema, TodoUpdateSchema
from fastapi import HTTPException, status


def get_all(db: Session, priority: TaskPriority | None = None):
    stmt = select(Todos).where(Todos.deleted == False)

    if priority:
        stmt = stmt.where(Todos.task_priority == priority)

    todos = db.execute(stmt).scalars().all()
    if not todos:
        raise HTTPException(
            status_code=status.HTTP_200_OK, detail="You're all caught up on your tasks.")
    return todos


def create(todo: TodoSchema, db: Session, user_id: int):
    todo_dict = todo.model_dump()

    todo_dict.update({"user_id": user_id})
    try:
        new_todo = Todos(
            **todo_dict
        )

        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return {"success": "Todo created successfully!"}
    except Exception as e:
        db.rollback()
        print(f"Some error occured: {e}")


def get_one(todo_id: int, db: Session):
    stmt = select(Todos).where(Todos.id == todo_id)

    todo = db.execute(stmt).scalars().first()
    if todo:
        return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="To-do not found.")


def delete(todo_id: int, db: Session):
    stmt = select(Todos).where(Todos.id == todo_id, Todos.deleted == False)

    todo = db.execute(stmt).scalars().first()
    if todo:
        todo.deleted = True
        db.commit()
        db.refresh(todo)
        return {}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="To do not found.")


def patch_update(todo_id: int, updated_todo: TodoUpdateSchema, db: Session):
    stmt = select(Todos).where(Todos.id == todo_id, Todos.deleted == False)

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
