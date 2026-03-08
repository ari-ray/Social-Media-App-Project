from fastapi import FastAPI
from backend.routes import users,posts
from fastapi.middleware.cors import CORSMiddleware
from backend.database import engine, Base

app = FastAPI()

app.add_middleware(
    CORSMiddleware, #Cross-Origin Resource Sharing: allows the frontend to talk to the backend.
    allow_origins=["*"], #allow all websites
    allow_credentials=True, #allow cookies/auth
    allow_methods=["*"], #allow GET POST PUT DELETE
    allow_headers=["*"], #allow all headers
)

Base.metadata.create_all(bind=engine)

# router = group of related endpoints
app.include_router(users.router, prefix="/users", tags=["users"]) #handles user stuff
app.include_router(posts.router, prefix="/api/posts", tags=["posts"]) #handles post stuff

@app.get("/")
def home():
    return {"message": "Social Media API is running"}
