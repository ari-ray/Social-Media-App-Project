# Routes

The routes directory handles all API routes for the app.

## Users (users.py)
- Register new users
- Log in and generate token-based sessions
- Fetch user details and list of users

## Posts (posts.py)
- CRUD operations for posts
- Like posts
- View Date and Time of the Post posted
- Search Posts (currently not exposed in the frontend)

## Key Features
- Token-based authentication for secure user actions
- CRUD operations for posts
- Like system to track interactions
- User permissions to ensure users can only edit/delete their own posts
- Search endpoint (backend only) for future expansion

## Future Improvements
- Expose the search functionality in the frontend
- Implement more advanced user analytics
