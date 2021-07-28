import datetime
from datetime import timezone
import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from .models import *


def index(request):
    return render(request, "network/index.html")


# return json response for all posts
@login_required(login_url="/login")
def get_all_posts(request):
    posts = Post.objects.all()
    posts = posts.order_by("-timestamp").all()
    json_obj = [post.serialize() for post in posts]
    return JsonResponse(json_obj, safe=False)


@csrf_exempt
@login_required(login_url="/login")
def get_post_by_id(request, post_id):
    try:
        post = Post.objects.get(id=int(post_id))
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize())
    
    elif request.method  == "PUT":
        data = json.loads(request.body)
        if data.get("likes") is not None:
            post.likes = data["likes"]
        if data.get("body") is not None:
            post.body = data["body"]
        post.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "GET or PUT request required"
        }, status=400)


@csrf_exempt
@login_required(login_url="/login")
def get_like_by_post_and_user_id(request, post_id, user_id):
    if request.method == "GET":
        try:
            like = Like.objects.get(post_pk=post_id, user_pk=user_id)
            return JsonResponse(like.serialize())
        except Like.DoesNotExist:
            return JsonResponse({"error": "Like not found"})

    elif request.method == "POST":
        like = Like.objects.create(user_pk=user_id, post_pk=post_id, unliked=False)
        if like.user_pk is not None and like.post_pk is not None:
            like.save()
        return HttpResponseRedirect(reverse("index"))

    elif request.method == "PUT":
        like = Like.objects.get(user_pk=user_id, post_pk=post_id)
        data = json.loads(request.body)
        if data.get("unliked") is not None:
            like.unliked = data["unliked"]
            like.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "GET, POST or PUT request required"
        }, status=400)


@login_required(login_url="/login")
def get_all_likes_by_post_id(request, post_id):
    try:
        likes = Like.objects.filter(post_pk=post_id)
        return JsonResponse([like.serialize() for like in likes], safe=False)
    except Like.DoesNotExist:
        return JsonResponse({"error": "Likes not found"})



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required(login_url="/login")
def submit_post(request):
    # TODO
    if request.method == "POST":
        body = request.POST.get("text", False)
        post = Post(
            poster=request.user.username,
            timestamp=datetime.datetime.now(timezone.utc),
            likes=0,
            body=body
        )
        if request.user.username is not None:
            post.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("index"))


def post_view():
    # TODO
    pass


def submit_comment():
    # TODO
    pass


def follow():
    # TODO
    pass


@login_required(login_url="/login")
def profile_view(request, profile_name):
    # TODO
    profile = User.objects.get(username=profile_name)
    posts = Post.objects.filter(poster=profile.username)
    if profile.username is not None:
        return render(request, "network/profile.html", {
            "profile": profile,
            "posts": posts
        })
    else:
        return render(request, "network/index.html")


@login_required(login_url="/login")
def get_profile(request, profile_name):
    profile = User.objects.get(username=profile_name)
    response = {
        "username": profile.username,
        "email": profile.email
    }
    return JsonResponse(response)


def edit_post_view():
    # TODO
    pass


def like():
    # TODO
    pass


def paginate():
    # TODO
    pass
