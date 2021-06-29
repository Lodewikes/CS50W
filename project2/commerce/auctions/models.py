from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    seller = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    description = models.TextField()
    start_bid = models.FloatField()
    listing_date = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)

    # Optional fields
    image = models.CharField(max_length=2048, default=None, blank=True, null=True)

    categories = [
        ("EL", "Electronics"),
        ("FA", "Fashion"),
        ("HB", "Health & Beauty"),
        ("HG", "Home & Garden"),
        ("SP", "Sports"),
        ("CA", "Collectables and Art"),
        ("IE", "Industrial Equipment"),
        ("MO", "Motors"),
        ("UN", "Uncategorized"),
    ]
    category = models.CharField(max_length=64, default=categories[-1],
                                blank=True, choices=categories)

    def __str__(self):
        return f"Listing: {self.title} by {self.seller}"


class Bid(models.Model):
    listing_pk = models.IntegerField()
    user = models.CharField(max_length=64)
    bid = models.FloatField()

    def __str__(self):
        return f"Bid: {self.user} bid {self.bid}"


class Comment(models.Model):
    user = models.CharField(max_length=64)
    comment = models.CharField(max_length=1000)
    listing_pk = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment: {self.user} commented at {self.time}"


class WatchList(models.Model):
    user = models.CharField(max_length=64)
    listing_pk = models.IntegerField()

    def __str__(self):
        return f"Watchlist: {self.user} listing id {self.listing_pk}"


class Sold(models.Model):
    pass
