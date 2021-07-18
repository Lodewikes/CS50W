from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    poster = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField()
    body = models.TextField()

    def __str__(self):
        return f"Post by {self.poster}"

    def is_likes_positive(self):
        return self.likes >= 0


# TODO determine necessity at later stage
# class Follower(models.Model):
#     pass
