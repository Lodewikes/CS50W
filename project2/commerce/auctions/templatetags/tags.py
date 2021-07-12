from django import template
from auctions.models import *
import datetime
from datetime import timezone
import math

from ..models import *

register = template.Library()


@register.simple_tag
def get_watchlist_status(user, pk):
    # Determine if a listing is already in watchlist
    obj = WatchList.objects.filter(user=user, listing_pk=int(pk))
    if obj:
        return True
    else:
        return False


@register.simple_tag
def get_watchlist_item(pk):
    # Based on the watchlist item's listing_pk return the listing object
    obj = AuctionListing.objects.get(id=int(pk))
    return obj


@register.simple_tag
def time_since_comment(timestamp):
    # Determine the time since a comment was created
    now = datetime.datetime.now(timezone.utc)
    difference = now - timestamp
    in_hours = difference.total_seconds() / 3600
    in_min = difference.total_seconds() / 60
    obj = []

    if in_hours > 24:
        days_float = in_hours / 24
        days_trunc = math.trunc(days_float)
        if days_trunc >= 30:
            obj.append(" month ago")
            obj.append("More than a")
        elif days_trunc == 1:
            obj.append("day")
        else:
            obj.append("days")
        obj.append(days_trunc)
        return obj

    elif in_hours < 24 and in_min > 60:
        hours_float = in_min / 60
        hours_trunc = math.trunc(hours_float)
        if hours_trunc == 1:
            obj.append("hour")
        else:
            obj.append("hours")
        obj.append(hours_trunc)
        return obj

    else:
        minutes_trunc = math.trunc(in_min)
        obj.append("min")
        obj.append(minutes_trunc)
        return obj


@register.simple_tag
def get_highest_bidder(listing_id):
    bids = Bid.objects.filter(listing_pk=int(listing_id))
    if bids:
        highest_bidding = bids[0]
        for bid in bids:
            print(bid)
            if highest_bidding is None or float(bid.bid) > highest_bidding.bid:
                highest_bidding = bid
        print(highest_bidding.bid)
        return highest_bidding
    else:
        return Bid(listing_pk=-1, user=None, bid=0)


@register.simple_tag
def get_category(listing_id):
    listing = AuctionListing.objects.get(id=int(listing_id))
    if listing is not None:
        category = listing.get_category_display()
        return category
    else:
        return "Uncategorized"

