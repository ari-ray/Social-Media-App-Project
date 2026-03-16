# Social Media App (SMAP) : https://smap-kfmy.onrender.com

A simple social media API built with FastAPI, SQLAlchemyand Pydantic. Supports user registration, login with token-based authentication, posting, liking, editing, deleting posts and searching posts. The Web-app has been deployed on Render.

## Features
- User Authentication
  - Register new users
  - Login and receive a secure token
  - Token-based authentication for post operations
- Posts Management
  - Create, read, update and delete posts
  - Like posts
  - Date and time stamps (UTC) on posts
- User Statistics
  - Get post count per user
 
## Tech Stack
- Backend: FastAPI
- Database ORM: SQLAlchemy
- Data Validation: Pydantic
- Server: Uvicorn

## Project Structure:
- Backend:
  - models.py : SQLAlchemy models (User, Post, Like, Session)
  - database.py : Database connection & base
  - routes
    - users.py : User registration, login, token handling
    - posts.py : CRUD operations, search, like functionality
- Frontend:
  - index.html : Main UI for posts
  - style.css : Styling for frontend
  - script.js : JS for API calls and DOM manipulation
- requirements.txt : Python dependencies
- README.md

## Installation
- Clone the repository
```bash
git clone <repo_url>
cd social-media-api
```
- Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```
- Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Project (Locally)
- Start the backend server:
```bash
uvicorn backend.main:app --reload
```
- Open the frontend in your browser:
  - Open frontend/index.html
  - Make sure "script.js" points to the correct backend URL (default: http://127.0.0.1:8000)

## API Endpoints
### Users
| Method | Endpoint | Description |
|------|------|------|
| POST | /users/register | Register a new user |
| POST | /users/login | Login user and get auth token |
| GET | /users/ | List all users |
| GET | /users/{username} | Get user by username |

### Posts
| Method | Endpoint | Description |
|------|------|------|
| POST | /api/posts/ | Create a post (token required) |
| GET | /api/posts/ | Get all posts |
| GET | /api/posts/search?keyword= | Search posts by keyword |
| GET | /api/posts/{post_id} | Get a specific post |
| PUT | /api/posts/{post_id} | Update a post (token required, owner only) |
| DELETE | /api/posts/{post_id} | Delete a post (token required, owner only) |
| POST | /api/posts/{post_id}/like | Like a post (token required) |
| GET | /api/posts/users/{user_id}/stats | Get post count of a user |

## Authentication
- Users receive a token on login
- Includes this token in requests requiring authentication:
```JavaScript
fetch(`${API_URL}/api/posts`, {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "token": localStorage.getItem("token")
    },
    body: JSON.stringify({ title: "My Post", content: "Hello world" })
});
```

## Frontend
- Simple HTML, CSS and JS frontend
- Users can:
  - Create posts
  - Edit and delete their posts
  - Like posts
  - Search posts by keyword
 
## Why This Project Matters
This project demonstrates the fundamentals of building a full-stack web application using modern backend technologies. It shows how to design and implement a API, handle authenticatoin and manage database interactions using an ORM.

Key learning outcomes from this project include:
- Building a backend API using FastAPI
- Structuring a scalable backend with routers and moddular architecture
- Managing databases using SQLAlchemy ORM
- Implementing token-based authentication
- Performing CRUD operations
- Connecitng a JavaSCript frontend to a backend API

The project also shows how backend systems handle real-world features such as post creation, liking content, searching data and enforcing user permissions for editing or deleting resources.

Overall this project serves as a practical example of how modern web applications manage users, data and authentication while maintaining clean and modular code.

## Limitations
- Frontend does not yet support "search by post title/content"
- Posts are not currently assciated with specific users
- System does not display which user is currently logged in

## IMPORTANT NOTE FOR DEPLOYMENT
While deploying the web-app on Render some challenges were faced. To overcome those challenges, some API_URL changes had to be done to the code. ALongside that, in order to get the frontend functional, all the frontend files are now put in the "static" folder of the "backend" directory. I have still left the "frontend" directory in here so that it is easier to distinguish the files. 
Oregon was selected as the region for deployment. 

## Author
Arittri Ray

Software Engineering | Building strong foundation in full-stack development


