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
            item.setAttribute("id", "post-" + post.id);
            setLikes(post);
            displayPost(post, item);
            document.querySelector("#list-posts").appendChild(item);
        })
    })
    .catch(error => console.log(error));
}

function displayPost(post, item) {
    const user_id = JSON.parse(document.getElementById("user_id").textContent);
    const user_name = JSON.parse(document.getElementById("user_name").textContent);
    poster = document.createElement("strong");
    timestamp = document.createElement("p");
    likes = document.createElement("p");
    bodyDiv = document.createElement("div");
    body = document.createElement("p");
    likeBtn = document.createElement("button");
    editPostBtn = document.createElement("button");

    // username
    poster.innerHTML = post.poster;
    poster.setAttribute("class", "like-btn")
    poster.addEventListener("click", () => displayProfile(post))
    
    // timestamp
    timestamp.innerHTML = post.timestamp;

    // body
    body.innerHTML = post.body;
    body.setAttribute("id", "post-body-" + post.id);
    body.style.whiteSpace = "pre-wrap";
    bodyDiv.setAttribute("id", "body-div-" + post.id)
    bodyDiv.appendChild(body);

    // likes
    likes.setAttribute("id", "post-likes-" + post.id)
    likes.innerHTML = post.likes;

    // like button

    likeBtn.setAttribute("class", "btn btn-dark");
    likeBtn.setAttribute("id", "likeBtn-" + post.id)
    likeBtn.style.marginRight = "5px";
    // set initial button text context
    fetch(`posts/likes/${post.id}/${user_id}`)
    .then(response => response.json())
    .then(like => {
        if(!like.error){
            if (!like.unliked) {
                document.getElementById("likeBtn-" + post.id).textContent = "Unlike";
            }
            else {
                document.getElementById("likeBtn-" + post.id).textContent = "Like";
            }
        }
        else {
            document.getElementById("likeBtn-" + post.id).textContent = "Like";
        }
    })
    likeBtn.addEventListener("click", () => likePost(post));

    // editPostBtn
    if (post.poster === user_name){
        editPostBtn.setAttribute("class", "btn btn-dark");
        editPostBtn.setAttribute("id", "editPostBtn-" + post.id);
        editPostBtn.textContent = "Edit";
        editPostBtn.addEventListener("click", () => editPost(post));
    }
    

    item.appendChild(document.createElement("hr"));
    item.appendChild(poster);
    item.appendChild(timestamp);
    item.appendChild(likes);
    item.appendChild(bodyDiv);
    item.appendChild(likeBtn);
    if (post.poster === user_name) {
        item.appendChild(editPostBtn);
    }
}

function displayProfile(post) {
    document.querySelector("#list-posts").innerHTML = "";
    document.querySelector("#list-posts").innerHTML = post.poster;
}

// likeBtn onclick handler
async function likePost(post) {
    const user_id = JSON.parse(document.getElementById("user_id").textContent);

    await fetch(`posts/likes/${post.id}/${user_id}`)
    .then(response => response.json())
    .then(like => {
        if (like.user_pk === undefined && like.post_pk === undefined && like.unliked === undefined) {
            likeFetch(post.id, user_id, "POST", false);
            console.log("create like");
            document.getElementById("likeBtn-" + post.id).textContent = "Unlike";
        }
        else if(like.user_pk !== undefined && like.post_pk !== undefined && like.unliked === false) {
            likeFetch(post.id, user_id, "PUT", true);
            console.log("unlike");
            document.getElementById("likeBtn-" + post.id).textContent = "Like";
        }
        else if(like.user_pk !== undefined && like.post_pk !== undefined && like.unliked === true) {
            likeFetch(post.id, user_id, "PUT", false);
            console.log("like");
            document.getElementById("likeBtn-" + post.id).textContent = "Unlike";
        } 
        console.log("setting likes")
        setLikes(post);
    });
}

// Called in likePost()
async function likeFetch(post_id, user_id, method, likeBool) {
    await fetch(`posts/likes/${post_id}/${user_id}`, {
        method: method,
        body: JSON.stringify({
            user_pk: user_id,
            post_pk: post_id,
            unliked: likeBool
        })
    })
    .then(response => response.json()) 
    .catch(error => console.log(error)); // FIXME SyntaxError: JSON.parse: unexpected end of data at line 1 column 1 of the JSON data index.js:132:29
}

async function setLikes(post) {
    var count = 0;
    await fetch(`posts/likes/${post.id}`)
    .then(response => response.json())
    .then(likes => {
        likes.forEach(like => {
            if (like.unliked === false) {
                count++;
            }
        });
        fetch(`posts/${post.id}`, {
            method: "PUT",
            body: JSON.stringify({
                likes: count
            })
        });
        document.getElementById("post-likes-" + post.id).innerHTML = post.likes;
    })
    .catch(error => console.log(error));
}

function editPost(post) {
    // get the elements to change
    const item = document.getElementById("post-" + post.id);
    const bodyDiv = document.getElementById("body-div-" + post.id);
    const body = document.getElementById("post-body-" + post.id);
    const editBtn = document.getElementById("editPostBtn-" + post.id);
    const saveBtn = document.createElement("button");

    // store text from body <p>
    var text = body.textContent;

    // remove the body <p>
    bodyDiv.removeChild(body);

    // replace editBtn with saveBtn
    item.removeChild(editBtn);
    saveBtn.setAttribute("class", "btn btn-primary");
    saveBtn.setAttribute("id", "save-edit-btn-" + post.id);
    saveBtn.textContent = "Save";
    item.appendChild(saveBtn);


    // create <textarea> to replace <p>
    const textarea = document.createElement("textarea");
    textarea.setAttribute("class", "form-control");
    textarea.setAttribute("id", "edit-post-textarea-" + post.id)
    textarea.textContent = text;
    textarea.style.marginBottom = "8px";
    textarea.style.width = "50%";
    textarea.style.whiteSpace = "pre-wrap"

    saveBtn.addEventListener("click", () => saveEditedPost(post))
    
    bodyDiv.appendChild(textarea);
}

async function saveEditedPost(post) {
    var textcontent = document.getElementById("edit-post-textarea-" + post.id).value;
    alert(textcontent)
    await fetch(`posts/${post.id}`, {
        method: "PUT",
        body: JSON.stringify({
            poster: post.poster,
            timestamp: post.timestamp,
            likes: post.likes,
            body: textcontent
        })
    })
    .then(response => response.json()) 
    .catch(error => console.log(error));
}