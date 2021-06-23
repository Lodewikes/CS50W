from django import template
from auctions.models import *

register = template.Library()


@register.simple_tag
def get_watchlist_status(user, pk):
    obj = WatchList.objects.filter(user=user, listing_pk=int(pk))
    if obj:
        return True
    else:
        return False


@register.simple_tag
def get_watchlist_item(pk):
    obj = AuctionListing.objects.get(id=int(pk))
    return obj
