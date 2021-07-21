document.addEventListener("DOMContentLoaded", function() {
    loadPosts();
});

function loadPosts() {
    document.querySelector("#list-posts").style.display = "block";

    fetch(`/posts`)
    .then(response => response.json())
    .then(posts => {
        posts.forEach(post => {
            const item = document.createElement("div");
            displayPosts(post, item);
            document.querySelector("#list-posts").appendChild(item);
        })
    })
}

function displayPosts(post, item) {
    poster = document.createElement("strong");
    timestamp = document.createElement("p");
    likes = document.createElement("p");
    body = document.createElement("p");
    likeBtn = document.createElement("button");

    // username
    poster.innerHTML = post.poster;
    poster.setAttribute("class", "like-btn")
    poster.addEventListener("click", () => displayProfile(post))
    
    // timestamp
    timestamp.innerHTML = post.timestamp;

    // body
    body.innerHTML = post.body;
    body.style.whiteSpace = "pre-wrap";

    // likes
    likes.innerHTML = post.likes;
    likes.setAttribute("id", "post-likes-" + post.id)

    // like button
    if (likeBtn.textContent !== "Unlike") {
        likeBtn.textContent = "Like";
    }
    likeBtn.setAttribute("class", "btn btn-dark");
    likeBtn.setAttribute("id", "likeBtn-" + post.id)
    likeBtn.addEventListener("click", () => likePost(post, likes))

    item.appendChild(poster);
    item.appendChild(timestamp);
    item.appendChild(likes);
    item.appendChild(body);
    item.appendChild(likeBtn);
    item.appendChild(document.createElement("hr"));
}

function displayProfile(post) {
    document.querySelector("#list-posts").innerHTML = "";
    document.querySelector("#list-posts").innerHTML = post.poster;
}

async function likePost(post, likesElement) {
    const user_id = JSON.parse(document.getElementById("user_id").textContent);

    // does like exist?
    // if so, unlike (PUT)
    // if not like the post (POST)
    // add or subract from total likes

    await fetch(`posts/likes/${post.id}/${user_id}`)
    .then(response => response.json())
    .then(like => {
        if (like.user_pk === undefined && like.post_pk === undefined && like.unliked === undefined) {
            likeFetch(post.id, user_id, "POST", false);
        }
        else if(like.user_pk !== undefined && like.post_pk !== undefined && like.unliked === false) {
            likeFetch(post.id, user_id, "PUT", true);
        }
        else if(like.user_pk !== undefined && like.post_pk !== undefined && like.unliked === true) {
            likeFetch(post.id, user_id, "PUT", false);
        } 
    })  
}

async function likeFetch(post_id, user_id, method, likeBool) {
    await fetch(`posts/likes/${post_id}/${user_id}`, {
        method: method,
        body: JSON.stringify({
            user_pk: user_id,
            post_pk: post_id,
            unliked: likeBool
        }),
    })
    .then(response => response.json())
    .catch(error => console.log(error));
}
