from fastapi import APIRouter #lets us create modular endpoints
from pydantic import BaseModel, EmailStr #used for defining the shape of incoming JSON and data validation
from typing import List #type hints
import secrets #generates random secure tokens for login sessions

router = APIRouter() #creates a mini-app just for users

user_db : List[dict] = [] #temporary db

tokens_db: dict = {} #maps token to username, used to check authentication when posting

class UserCreate(BaseModel): #data that a user must send when creating an account
    username: str
    email: EmailStr

class UserLogin(BaseModel): #defines structure for logging in
    username: str

@router.post("/register")
def register_user(user: UserCreate):
    for u in user_db: #check for duplicate username
        if u["username"] == user.username:
            return {"error": "Username already exists"}
    user_db.append(user.dict())
    return {
        "message": "User registered",
        "user": user
    }

@router.post("/login")
def login_user(user: UserLogin): #check if username exists in users_db
    if not any(u["username"] == user.username for u in user_db):
        return {"error": "User does not exist"}
    token = secrets.token_hex(8)
    tokens_db[token] = user.username
    return{
        "message" : "Login successful",
        "token": token
    }

















