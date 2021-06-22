from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/closed", views.closed_listings, name="closed_listings"),
    path("listings/create", views.create_listing, name="create_listing"),
    path("categories", views.categories, name="categories")
]
