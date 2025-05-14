from fastapi import APIRouter, status, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from ..database.connection import get_db
from ..core import authentication
from ..schemas.authentication_schemas import Token
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]) -> Token:
    authenticated_user = authentication.authenticate_user(
        form_data.username, form_data.password, db)

    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials!")
    access_token = authentication.create_access_token(
        data={"sub": str(authenticated_user.id)}
    )
    return Token(access_token=access_token, token_type="bearer")
