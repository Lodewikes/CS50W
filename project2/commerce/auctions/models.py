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

    # Optional fields
    image = models.CharField(max_length=2048, default=None, blank=True, null=True)
    category = models.CharField(max_length=64, default="uncategorized", blank=True)

    def __str__(self):
        return f"Listing: {self.title} by {self.seller}"


class Bid(models.Model):
    listing_pk = models.IntegerField()
    user = models.CharField(max_length=64)
    bid = models.FloatField()


class Comment(models.Model):
    user = models.CharField(max_length=64)
    comment = models.CharField(max_length=1000)
    listing_pk = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)


class WatchList(models.Model):
    user = models.CharField(max_length=64)
    listing_pk = models.IntegerField()


class Sold(models.Model):
    pass
