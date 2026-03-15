from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from backend.database import Base

class User(Base):
    __tablename__ = "users"  # Name of the table in the DB
    id = Column(Integer, primary_key=True, index=True)  # primary key, indexed
    username = Column(String(50), unique=True, index=True)  # unique username
    email = Column(String(100), unique=True, index=True)     # unique email
    posts = relationship("Post", back_populates="owner")  # links to all posts by this user
    likes = relationship("Like", back_populates="user")   # links to all likes by this user
    sessions = relationship("Session", back_populates="user")

class Post(Base):
    __tablename__ = "posts"
    title = Column(String(200))
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)  # the text content of the post
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # timestamp
    likes_count = Column(Integer, default=0)  # number of likes
    owner_id = Column(Integer, ForeignKey("users.id"))  # references the user's id
    owner = relationship("User", back_populates="posts")  # links back to the user
    likes = relationship("Like", back_populates="post")  # links to likes for this post

class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")
    __table_args__ = (UniqueConstraint("user_id", "post_id", name="unique_user_post"),)

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(64), unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    expires_at = Column(DateTime)
    user = relationship("User", back_populates="sessions")
