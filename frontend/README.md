# Frontend

This directory contains the frontend of the social media app built with HTML, CSS and vanilla JavaScript. It interacts with backend API to allow users to:
- Register
- Login
- Create Posts
- View Posts
- Edit their own posts
- Delete their own posts

NOTE: Search functionality exists in the backend but is not currently exposed in the UI.

## How it Works
- Users register or log in, receiving a token thay is stored
- The token is used in headers for all API requests, ensuring authentication
- Users can perform CRUD operations directly from frontend
- Posts are displayed in descending order by creation time

## Future Improvements
- Add a search to query posts by title or content
- Impove UI/UX for mobile respnsiveness

