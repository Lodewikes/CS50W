
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts/post", views.submit_post, name="post"),
    path("posts", views.get_all_posts, name="get_posts"),
    path("posts/<str:post_id>", views.get_post_by_id, name="get_post_bt_id"),
    path("profile/<str:profile_name>", views.profile_view, name="profiles"),
    path("posts/likes/<str:post_id>", views.get_all_likes_by_post_id, name="post_likes"),
    path("posts/likes/<str:post_id>/<str:user_id>", views.get_like_by_post_and_user_id, name="post_like_by_user"),
]
