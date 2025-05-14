from fastapi import APIRouter, status, Depends, Path
from typing import Annotated
from ..schemas.user_schemas import UserSchema, ShowUserSchema, UserUpdateSchema
from ..schemas.relationship_schemas import ShowUserRelSchema
from ..handlers import user_handler
from sqlalchemy.orm import Session
from ..database.connection import get_db
from ..core.authentication import verify_token, is_Admin

router = APIRouter()


@router.post("/create_user/", status_code=status.HTTP_201_CREATED)
def create_user(request: UserSchema, db: Annotated[Session, Depends(get_db)]):
    return user_handler.create_user(request, db)


@router.get("/user_profile/", status_code=status.HTTP_200_OK, response_model=ShowUserRelSchema)
def get_user_data(user_id: Annotated[int, Depends(verify_token)], db: Annotated[Session, Depends(get_db)]):
    return user_handler.get_user(user_id, db)


@router.patch("/user_profile/", status_code=status.HTTP_200_OK, response_model=ShowUserSchema)
def update_user_profile(user_id: Annotated[int, Depends(verify_token)], updated_user: UserUpdateSchema, db: Annotated[Session, Depends(get_db)]):
    return user_handler.update_user(user_id, updated_user, db)


@router.get("/admin_specific/", status_code=status.HTTP_200_OK, response_model=list[ShowUserSchema], dependencies=[Depends(is_Admin)])
def get_all_user_data(db: Annotated[Session, Depends(get_db)]):
    return user_handler.get_all_user(db)


@router.delete("/admin/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(is_Admin)])
def delete_todo(user_id: Annotated[int, Path()], db: Annotated[Session, Depends(get_db)]):
    return user_handler.delete_user(user_id, db)
