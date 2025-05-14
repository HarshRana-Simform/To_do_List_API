from ..schemas.user_schemas import UserSchema, UserUpdateSchema
from ..models.user_models import User
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..core import authentication
from fastapi import HTTPException, status


def create_user(request: UserSchema, db: Session):

    request.password = authentication.get_password_hash(request.password)

    try:
        new_user = User(
            **request.model_dump()
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"An error occured: Username already exists!")
    return {"success": f"User: {request.username} created successfully!"}


def get_user(user_id: int, db: Session):
    stmt = select(User).where(User.id == user_id, User.deleted == False)
    user = db.execute(stmt).scalars().first()

    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found.")


def get_all_user(db: Session):
    stmt = select(User).where(User.deleted == False)
    users = db.execute(stmt).scalars().all()

    if users:
        return users
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="No users found.")


def update_user(user_id: int, updated_user: UserUpdateSchema, db: Session):
    stmt = select(User).where(User.id == user_id, User.deleted == False)
    user = db.execute(stmt).scalars().first()

    if user:
        if updated_user.username is not None:
            user.username = updated_user.username
        if updated_user.email is not None:
            user.email = updated_user.email
        if updated_user.password is not None:
            updated_user.password = authentication.get_password_hash(
                updated_user.password)
            user.password = updated_user.password

        db.commit()
        db.refresh(user)

        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found.")


def delete_user(user_id: int, db: Session):
    stmt = select(User).where(User.id == user_id, User.deleted == False)

    user = db.execute(stmt).scalars().first()
    if user:
        user.deleted = True
        db.commit()
        db.refresh(user)
        return {}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found.")
