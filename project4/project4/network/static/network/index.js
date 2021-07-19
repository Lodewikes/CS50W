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

    // likes
    likes.innerHTML = post.likes;

    // like button
    likeBtn.textContent = "Like";
    likeBtn.setAttribute("class", "btn btn-dark");

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