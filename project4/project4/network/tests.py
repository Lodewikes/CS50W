import datetime
from datetime import timezone

from django.test import Client, TestCase

from .models import User, Post


# Create your tests here.
class PostTestCase(TestCase):

    def setUp(self):

        # create users
        personA = User.objects.create_user(
            username="Harold",
            email="Harold@son.com",
            password="harold"
        )
        personB = User.objects.create_user(
            username="Kumar",
            email="kumar@son.com",
            password="kumar"
        )

        # create posts
        postA = Post.objects.create(
            poster=personA.username,
            timestamp=datetime.datetime.now(timezone.utc),
            likes=0,
            body="This is PostA"
        )

        postB = Post.objects.create(
            poster=personB.username,
            timestamp=datetime.datetime.now(timezone.utc),
            likes=-1,
            body="This is PostB"
        )

        postC = Post.objects.create(
            poster=personB.username,
            timestamp=datetime.datetime.now(timezone.utc),
            likes=1,
            body="This is PostC"
        )

    def test_negative_likes(self):
        post = Post.objects.get(poster="Kumar", likes=-1)
        self.assertFalse(post.is_likes_positive())

    def test_zero_likes(self):
        post = Post.objects.get(poster="Harold")
        self.assertTrue(post.is_likes_positive())

    def test_positive_likes(self):
        post = Post.objects.get(poster="Kumar", likes=1)
        self.assertTrue(post.is_likes_positive())

    def test_index_view(self):
        c = Client()
        response = c.get("")
        self.assertEqual(response.status_code, 200)
