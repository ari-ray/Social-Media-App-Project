from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from backend.database import get_db
from backend.models import User, Post, Like

router = APIRouter()

class PostCreate(BaseModel): #creating or updating a post
    title: str
    content: str

class PostOut(BaseModel): #sending post data back to the frontend.
    id: int
    title: str
    content: str
    owner_id: int
    created_at: datetime
    likes_count: int

    class Config:
        from_attributes = True

from .users import get_current_user #get the logged-in user from a token

@router.post("/", response_model=PostOut)
def create_post(post: PostCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_post = Post(
        title=post.title,
        content=post.content,
        owner_id=current_user.id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/", response_model=List[PostOut]) #fetches all posts from the database
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).order_by(Post.created_at.desc()).all()
    return posts

@router.get("/search", response_model=List[PostOut]) #searches posts by title or content
def search_posts(keyword: str, db: Session = Depends(get_db)):
    posts = db.query(Post).filter(Post.title.ilike(f"%{keyword}%") | Post.content.ilike(f"%{keyword}%")).all()
    return posts

@router.get("/{post_id}", response_model=PostOut) #fetches one post nby post_id
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=PostOut) #updates a post
def update_post(post_id: int, post_data: PostCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot edit others' posts")

    post.title = post_data.title
    post.content = post_data.content
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{post_id}")
def delete_post(post_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot delete others' posts")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}

@router.post("/{post_id}/like")
def like_post(post_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    existing_like = db.query(Like).filter(Like.user_id == current_user.id, Like.post_id == post_id).first()
    if existing_like:
        raise HTTPException(status_code=400, detail="You already liked this post")

    new_like = Like(user_id=current_user.id, post_id=post_id)
    post.likes_count += 1
    db.add(new_like)
    db.commit()
    db.refresh(post)
    return {"message": "Post liked", "likes_count": post.likes_count}


@router.get("/users/{user_id}/stats")
def user_stats(user_id: int, db: Session = Depends(get_db)):
    count = db.query(Post).filter(Post.owner_id == user_id).count()
    return {"user_id": user_id, "post_count": count}
