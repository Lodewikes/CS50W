from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/close/<str:listing_id>", views.close_listing, name="close_listing"),
    path("listings/closed", views.closed_listings, name="closed_listings"),
    path("listings/create", views.create_listing, name="create_listing"),
    path("listings/<str:listing_id>", views.listing_view, name="listing"),
    path("categories", views.categories, name="categories"),
    path("watchlist/add/<str:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("listing/comment/<str:listing_id>", views.post_comment, name="post_comment"),
    path("listing/bid/<str:listing_id>", views.bid, name="bid"),
    path("categories/<str:category>", views.single_category_view, name="category")
]
