from django import template
from auctions.models import *

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_watchlist_status(user, pk):
    obj = WatchList.objects.filter(user=user, listing_pk=int(pk))
    if obj:
        return True
    else:
        return False
