from fastapi import APIRouter, Header # APIRouter: modular endpoints & Header: used to read HTTP headers for token
from pydantic import BaseModel #data validation
from typing import List
from .users import user_db, tokens_db #to access the registered users and verify tokens


router = APIRouter() #mini app

posts_db: List[dict] = [] #temp db

class PostCreate(BaseModel): #basic structure for posts
    title : str
    content : str

@router.post("/create")
def create_post(post: PostCreate, token: str = Header(...)): #reads header named token
    if token not in tokens_db: #validates the token in the db
        return {"error" : "Invalid or missing token"}
    owner = tokens_db[token] #adds username as post owner
    post_data = post.dict()
    post_data["owner"] = owner
    posts_db.append(post_data)
    return {"message": "Post created", "post": post_data}


@router.get("/") #to get the posts
def get_posts():
    return {
        "posts" : posts_db
    }
