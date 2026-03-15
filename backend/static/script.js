const API_URL = "https://smap-kfmy.onrender.com";
const token = localStorage.getItem("token");

if (!token) {
    window.location.href = "login.html";
}

// async = handles asynchronous operations
async function fetchPosts() {//res is the whole HHTp response object we get from the server and data contains the posts array
    try {
        const res = await fetch(`${API_URL}/api/posts`); //fetch sends a GET request to /posts endpoint
        const posts = await res.json(); //res.json(): parses the response as JSON & data hold the posts array from backend


         if (!Array.isArray(posts)) {
            console.error("Expected array, got:", posts);
            return;
        }

        const postsDiv = document.getElementById("posts");
        postsDiv.innerHTML = "";

        posts.forEach(post => {
            const div = document.createElement("div");
            div.innerHTML = `
                <h3>${post.title}</h3>
                <p>${post.content}</p>
                <small>${new Date(post.created_at).toLocaleString()}</small>
                <br>
                <button onclick="likePost(${post.id})">❤️ ${post.likes_count}</button>
                <button onclick="editPost(${post.id})">✏️ Edit</button>
                <button onclick="deletePost(${post.id})">🗑 Delete</button>
                <hr>
            `;
            postsDiv.appendChild(div);
        });
    } catch (e) {
        alert("Error loading posts: " + e.message);
    }
}

async function createPost() {
    const content = document.getElementById("content").value.trim();
    if (!content) {
        alert("Post cannot be empty");
        return;
    }

    try {
        await fetch(`${API_URL}/api/posts`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "token": token
            },
            body: JSON.stringify({
                title: "Post",
                content: content
            })
        });
        document.getElementById("content").value = "";
        fetchPosts();
    } catch (e) {
        alert("Error creating post: " + e.message);
    }
}

async function likePost(id) {
    try {
        await fetch(`${API_URL}/api/posts/${id}/like`, {
            method: "POST",
            headers: { "token": token }
        });
        fetchPosts();
    } catch (e) {
        alert("Error liking post");
    }
}

async function deletePost(id) {
    if (!confirm("Delete this post?")) return;
    try {
        await fetch(`${API_URL}/api/posts/${id}`, {
            method: "DELETE",
            headers: { "token": token }
        });
        fetchPosts();
    } catch (e) {
        alert("Error deleting post");
    }
}

async function editPost(id) {
    const newContent = prompt("Edit post content:");
    if (!newContent?.trim()) return;

    try {
        await fetch(`${API_URL}/api/posts/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "token": token
            },
            body: JSON.stringify({
                title: "Updated Post",
                content: newContent
            })
        });
        fetchPosts();
    } catch (e) {
        alert("Error editing post");
    }
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}

// Load posts on page load
fetchPosts();
