
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts/post", views.submit_post, name="post"),
    path("posts", views.get_all_posts, name="get_posts"),
    path("profile/<str:profile_name>", views.profile_view, name="profiles"),
]
