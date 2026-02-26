from fastapi import FastAPI
from backend.routes import users,posts

app = FastAPI()

# router = group of related endpoints
app.include_router(users.router) #handles user stuff
app.include_router(posts.router) #handles post stuff

@app.get("/")
def home():
    return {"message": "API is running"}