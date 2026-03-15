# Backend

The backend is built with FastAPI and uses SQLAlchemy for database management.

## Key Features
- Modular structure using APIRouter
- Token-based authentication for secure endpoints
- CRUD operations for posts
- Like and search functionality for posts
- Database models for users, posts and likes
- User stats (number of posts)

## Setup
- Install dependencies:
```bash
pip install -r requirements.txt
```
- Start the FastAPI server:
```bash
uvicorn backend.main:app --reload
```
- API will be available at http://127.0.0.1:8000
  
