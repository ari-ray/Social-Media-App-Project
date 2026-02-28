from fastapi import APIRouter, Header, HTTPException # APIRouter: modular endpoints & Header: used to read HTTP headers for token
from pydantic import BaseModel #data validation
from typing import List
from .users import tokens_db #to access registered users an verify tokens
from datetime import datetime, timezone #for timestamping the posts

router = APIRouter() #mini app
posts_db: List[dict] = [] #temp db

class PostCreate(BaseModel): #basic struct for posts
    title: str
    content: str

@router.post("/posts") #to create post
def create_post(post: PostCreate, token: str = Header(...)):
    if token not in tokens_db:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    owner = tokens_db[token]
    post_data = post.model_dump()
    post_data["owner"] = owner
    post_data["created_at"] = datetime.now(timezone.utc).isoformat()
    post_data["likes"] = 0  #initialize likes
    posts_db.append(post_data)
    return {"message": "Post created", "post": post_data}


@router.get("/posts") #to get sorted posts
def get_posts():
    sorted_posts = sorted(
        posts_db,
        key=lambda x: x["created_at"],
        reverse=True
    )
    return {"posts": sorted_posts}


@router.get("/posts/{post_id}") #to find specific posts
def get_post(post_id: int):
    if post_id >= len(posts_db) or post_id < 0:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"post": posts_db[post_id]}


@router.get("/users/{username}/posts") #to get posts of pecific user
def get_posts_by_user(username: str):
    user_posts = [p for p in posts_db if p["owner"] == username]
    return {"posts": user_posts}


@router.put("/posts/{post_id}") #to update post
def update_post(post_id: int, post: PostCreate, token: str = Header(...)):
    if token not in tokens_db:
        raise HTTPException(status_code=401, detail="Invalid token")
    owner = tokens_db[token]
    if post_id >= len(posts_db) or post_id < 0:
        raise HTTPException(status_code=404, detail="Post not found")
    if posts_db[post_id]["owner"] != owner:
        raise HTTPException(status_code=403, detail="Cannot edit others' posts")
    posts_db[post_id].update(post.model_dump())
    return {"message": "Post updated", "post": posts_db[post_id]}


@router.delete("/posts/{post_id}") #to delete post
def delete_post(post_id: int, token: str = Header(...)):
    if token not in tokens_db:
        raise HTTPException(status_code=401, detail="Invalid token")
    owner = tokens_db[token]
    if post_id >= len(posts_db) or post_id < 0:
        raise HTTPException(status_code=404, detail="Post not found")
    if posts_db[post_id]["owner"] != owner:
        raise HTTPException(status_code=403, detail="Cannot delete others' posts")
    deleted_post = posts_db.pop(post_id)
    return {"message": "Post deleted", "post": deleted_post}


@router.post("/posts/{post_id}/like") #to like post
def like_post(post_id: int):
    if post_id >= len(posts_db) or post_id < 0:
        raise HTTPException(status_code=404, detail="Post not found")
    posts_db[post_id]["likes"] += 1
    return {"message": "Post liked", "post": posts_db[post_id]}

@router.get("/posts/search") #to search post
def search_posts(keyword: str):
    results = [p for p in posts_db if keyword.lower() in p["title"].lower()]
    return {"results": results}

@router.get("/users/{username}/stats") #post count per user
def user_stats(username: str):
    count = len([p for p in posts_db if p["owner"] == username])
    return {"username": username, "post_count": count}

