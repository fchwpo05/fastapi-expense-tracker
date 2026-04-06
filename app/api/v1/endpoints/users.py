from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token
from typing import cast
from app.core.dependencies import get_current_user
from app.services import user_service

router = APIRouter()

@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.create_user(db=db, user_in=user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.login_user(db=db, user_in=user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user