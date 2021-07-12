import datetime
from datetime import timezone

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import template

from .models import *

categories_list = [
    "Electronics",
    "Fashion",
    "Health & Beauty",
    "Home & Garden",
    "Sports",
    "Collectables and Art",
    "Industrial Equipment",
    "Motors",
    "Uncategorized",
]


def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.all(),
        "bids": Bid.objects.all()
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


@login_required(login_url="/login")
def closed_listings(request):
    return render(request, "auctions/closedListings.html", {
        "listings": AuctionListing.objects.all(),
        "bids": Bid.objects.all()
    })


@login_required(login_url="/login")
def close_listing(request, listing_id):
    listing = AuctionListing.objects.get(id=int(listing_id))
    if listing and listing.seller == request.user.username:
        listing.closed = True
        listing.save()
    return render(request, "auctions/closedListings.html", {
        "listings": AuctionListing.objects.all(),
        "bids": Bid.objects.all()
    })


def categories(request):
    for category in categories_list:
        # TODO
        pass
    return render(request, "auctions/categories.html", {
        "categories_list": categories_list,
        "listings": AuctionListing.objects.all(),
    })


def single_category_view(request, category):
    categories_item = [category]
    return render(request, "auctions/categories.html", {
        "categories_list": categories_item,
        "listings": AuctionListing.objects.all()
    })
    pass


@login_required(login_url="/login")
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        start_bid = request.POST["starting_bid"]
        image = request.POST["image_url"]
        description = request.POST["text"]
        category = request.POST["category_dropdown"]

        categries = AuctionListing().categories
        i = 0
        for i in range(len(categries)):
            print(category)
            if category == categries[i][1]:
                print(categries[i][1])
                listing = AuctionListing(title=title, description=description,
                                         start_bid=start_bid, image=image, category=categries[i][1],
                                         seller=request.user.username, listing_date=datetime.datetime.now(timezone.utc))
                if request.user.username is not None:
                    listing.save()
                return render(request, "auctions/index.html", {
                    "listings": AuctionListing.objects.all(),
                    "bids": Bid.objects.all()
                })
            i += 1
    else:
        return render(request, "auctions/createListing.html", {
            "categories": categories_list
        })


@login_required(login_url="/login")
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
        return render(request, "auctions/index.html", {
            "listings": AuctionListing.objects.all(),
            "bids": Bid.objects.all()
        })
    else:
        new_item = WatchList(user=request.user.username, listing_pk=listing_id)
        new_item.save()
        return render(request, "auctions/index.html", {
            "listings": AuctionListing.objects.all(),
            "bids": Bid.objects.all()
        })


@login_required(login_url="/login")
def post_comment(request, listing_id):
    if request.method == "POST":
        comment = request.POST.get("text", False)
        user = request.user.username
        time = datetime.datetime.now(timezone.utc)
        comment_obj = Comment(user=user, comment=comment, listing_pk=int(listing_id), time=time)
        if user is not None:
            comment_obj.save()
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="/login")
def bid(request, listing_id):
    # FIXME stop accepting bids below starting bid
    if request.method == "POST":
        bids = Bid.objects.filter(listing_pk=listing_id)
        highest_bid = None
        if bids:
            for bidding in bids:
                if highest_bid is None or bidding.bid > highest_bid:
                    highest_bid = bidding.bid
        else:
            highest_bid = None

        bid = Bid(listing_pk=int(listing_id), user=request.user.username, bid=request.POST.get("bid", False))
        if request.user.username is not None and highest_bid is None and float(bid.bid) > float(
                AuctionListing.objects.get(id=int(listing_id)).start_bid):
            bid.save()
            return render(request, "auctions/listing.html", {
                "listing": AuctionListing.objects.get(pk=int(listing_id)),
                "comments": Comment.objects.all().filter(listing_pk=int(listing_id)),
            })
        elif request.user.username is not None and highest_bid is not None and float(bid.bid) > float(highest_bid):
            bid.save()
            return render(request, "auctions/listing.html", {
                "listing": AuctionListing.objects.get(pk=int(listing_id)),
                "comments": Comment.objects.all().filter(listing_pk=int(listing_id)),
            })
        else:
            return render(request, "auctions/listing.html", {
                "listing": AuctionListing.objects.get(pk=int(listing_id)),
                "comments": Comment.objects.all().filter(listing_pk=int(listing_id)),
                "failed_bid_message": "Bid must be higher than the starting and current bid"
            })
