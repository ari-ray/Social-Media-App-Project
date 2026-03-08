from fastapi import APIRouter, HTTPException, Depends, Header #APIRouter: lets us create modular endpoints, Depends: allows automatic injection of the DB session
from pydantic import BaseModel, EmailStr
from typing import List
from sqlalchemy.orm import Session #Factory for creating SQLAlchemy sessions
from backend.database import SessionLocal
from backend.models import User, Session as DBSession
from datetime import datetime, timezone, timedelta
import secrets

router = APIRouter()
SessionLocal = SessionLocal


def get_db(): #Each request will request a new DB session
    db = SessionLocal()
    try:
        yield db #ensures session is properly closed after request
    finally:
        db.close()


class UserCreate(BaseModel): #registration
    username: str
    email: EmailStr


class UserLogin(BaseModel): #login
    username: str


class UserOut(BaseModel): #output responses
    id: int
    username: str
    email: str


def get_current_user(token: str = Header(..., alias="token"), db: Session = Depends(get_db)): #validate token from headers and return the corresponding user object
    now = datetime.now(timezone.utc)
    db_session = db.query(DBSession).filter(
        DBSession.token == token,
        DBSession.expires_at > now
    ).first()

    if not db_session:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == db_session.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.post("/register", response_model=dict)
def register_user(user: UserCreate, db: Session = Depends(get_db)): #register a new user
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "message": "User registered",
        "user": {"id": db_user.id, "username": db_user.username}
    }


@router.post("/login", response_model=dict)
def login_user(user: UserLogin, db: Session = Depends(get_db)): #log in an existing user
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User does not exist")

    token = secrets.token_hex(32)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=24)

    db_session = DBSession(token=token, user_id=db_user.id, expires_at=expires_at)
    db.add(db_session)
    db.commit()

    return {"message": "Login successful", "token": token}


@router.get("/", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)): #fetch and return a list of all users
    users = db.query(User).all()
    return [{"id": u.id, "username": u.username, "email": u.email} for u in users]


@router.get("/{username}", response_model=UserOut)
def get_user(username: str, db: Session = Depends(get_db)): #fetch and return a single user by username
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not done")
    return {"id": user.id, "username": user.username, "email": user.email}
