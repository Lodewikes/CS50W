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

function likePost(post, likesElement) {
    // TODO refresh resets btn to like
    // TODO make sure like/unlike is for logged in user only and not affect other users
    var likes_nr;
    var btn = document.querySelector("#likeBtn-" + post.id);
    if (btn.textContent === "Like") {
        likes_nr = post.likes += 1;
        btn.textContent = "Unlike";
    }
    else if (btn.textContent === "Unlike") {
        likes_nr = post.likes -= 1;
        btn.textContent = "Like";
    }
    fetch(`/posts/${post.id}`, {
        method: "PUT",
        body: JSON.stringify({
            likes: likes_nr,
        })
    })
    .catch(error => console.log(error));
    document.querySelector("#post-likes-" + post.id).innerHTML = likes_nr;
}
