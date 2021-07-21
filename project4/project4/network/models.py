from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    poster = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField()
    body = models.TextField()

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster,
            "timestamp": self.timestamp,
            "likes": self.likes,
            "body": self.body
        }

    def __str__(self):
        return f"Post by {self.poster}"

    def is_likes_positive(self):
        return self.likes >= 0


# TODO determine necessity at later stage
# class Follower(models.Model):
#     pass

class Like(models.Model):
    user_pk = models.IntegerField()
    post_pk = models.IntegerField()
    unliked = models.BooleanField(default=False)

    def __str__(self):
        return f"User {self.user_pk} liked post {self.post_pk}"

    def serialize(self):
        return {
            "id": self.id,
            "user_pk": self.user_pk,
            "post_pk": self.post_pk,
            "unliked": self.unliked
        }
