from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime

from ..database import get_db, User

router = APIRouter()


# Pydantic models for request/response
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserListResponse(BaseModel):
    users: List[UserResponse]


# Endpoints
@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username or email already exists
    existing_user = (
        db.query(User)
        .filter((User.username == user.username) | (User.email == user.email))
        .first()
    )

    if existing_user:
        if existing_user.username == user.username:
            raise HTTPException(status_code=400, detail="Username already registered")
        else:
            raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    db_user = User(username=user.username, email=user.email)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.get("/users", response_model=UserListResponse)
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return {"users": users}


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserBase, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if username or email already exists for another user
    existing_user = (
        db.query(User)
        .filter(
            (
                (User.username == user_update.username)
                | (User.email == user_update.email)
            )
            & (User.id != user_id)
        )
        .first()
    )

    if existing_user:
        if existing_user.username == user_update.username:
            raise HTTPException(status_code=400, detail="Username already taken")
        else:
            raise HTTPException(status_code=400, detail="Email already registered")

    # Update user attributes
    db_user.username = user_update.username
    db_user.email = user_update.email

    db.commit()
    db.refresh(db_user)

    return db_user


@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()

    return {"message": "User deleted successfully"}


# Function to create a default user if none exists
def create_default_user(db: Session):
    # Check if any users exist
    if db.query(User).count() > 0:
        return

    # Create default user
    default_user = User(username="default_user", email="user@example.com")

    db.add(default_user)
    db.commit()
    db.refresh(default_user)

    return default_user
