from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import template

from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.all(),
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def closed_listings(request):
    return render(request, "auctions/closedListings.html")


def categories(request):
    return render(request, "auctions/categories.html")


def create_listing(request):
    return render(request, "auctions/createListing.html")


def listing_view(request, listing_id):
    return render(request, "auctions/listing.html", {
        "listing": AuctionListing.objects.get(pk=int(listing_id)),
        "comments": Comment.objects.all().filter(listing_pk=int(listing_id))
    })


@login_required(login_url="/login")
def watchlist_view(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": WatchList.objects.all().filter(user=request.user.username)
    })


@login_required(login_url="/login")
def add_to_watchlist(request, listing_id):
    item = WatchList.objects.filter(user=request.user.username, listing_pk=listing_id)

    if item:
        item.delete()
        print("removed")
        # return render(request, "auctions/index.html", {
        #     "listings": AuctionListing.objects.all(),
        # })
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        new_item = WatchList(user=request.user.username, listing_pk=listing_id)
        new_item.save()
        print("added")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
