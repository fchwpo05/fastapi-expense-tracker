from sqlalchemy.orm import Session
from typing import Optional

from app.db.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_in: UserCreate) -> User:
    existing_user = get_user_by_email(db, user_in.email)
    if existing_user:
        raise ValueError("Email already registered")

    db_user = User(
        email=user_in.email,
        name=user_in.name,
        hashed_password=hash_password(user_in.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def login_user(db: Session, user_in: UserCreate):
    user = authenticate_user(db, user_in.email, user_in.password)

    if not user:
        raise ValueError("Invalid credentials")

    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }