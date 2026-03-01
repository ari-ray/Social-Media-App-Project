const API_URL = "http://127.0.0.1:8000";

// async = handles asynchronous operations
async function fetchPosts(){ //res is the whole HHTp response object we get from the server and data contains the posts array
    const res = await fetch(`${API_URL}/posts`); //fetch sends a GET request to /posts endpoint
    const data = await res.json(); //res.json(): parses the response as JSON & data hold the posts array from backend

    //clearing old posts
    const postsDiv = document.getElementById("posts");
    postsDiv.innerHTML = ""; //clears the div first so that posts dont get duplicated

    //display
    data.forEach(post => { //loop
        const div = document.createElement("div"); //creates new div element in memory which holds one post
        div.innerHTML = `
            <p>${post.content}</p>
            <small>${new Date(post.created_at).toLocaleString()}</small>
            <button onclick="likePost(${post.id})">
                ❤️${post.likes}
            </button>

            <button onclick="editPost(${post.id})">
        ✏️      Edit
            </button>

            <button onclick="deletePost(${post.id})">
                🗑 Delete
            </button>
            <hr>
        `;
        postsDiv.appendChild(div);
    });
}

//create post
async function createPost(){
    const content = document.getElementById("content").value; //finds <input> with id="content" reads whatever is typed there and then stores it in the variable 'content'

    if (!content.trim()) {
        alert("Post cannot be empty");
        return;
    }

    await fetch(`${API_URL}/posts`,{
        method: "POST", //sends a POST request to /posts endpoint
        headers: {
            "Content-Type" : "application/json" //backend knows it's JSON
        },
        body: JSON.stringify({ content }) //sends the typed text in JSON format
    });

    document.getElementById("content").value =""; //clears the input
    fetchPosts()
}

//likes
async function likePost(id){
    await fetch(`${API_URL}/posts/${id}/like`, {
       method: "POST" //sends a post request and updates on backend
    });
    fetchPosts(); //refreshes posts with updated likes
}

async function deletePost(id){
    await fetch(`${API_URL}/posts/${id}`, {
        method: "DELETE"
    });

    fetchPosts();
}

async function editPost(id){
    const currentText = document.getElementById(`content-${id}`).innerText;

    const newContent = prompt("Edit your post:", currentText);

    if (!newContent || !newContent.trim()) return;

    await fetch(`${API_URL}/posts/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ content: newContent })
    });

    fetchPosts();
}

fetchPosts();

