from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.get_wiki, name="get_wiki"),
    path("wiki/<str:title>/edit", views.edit_entry, name="edit"),
    path("create", views.new_entry, name="new_entry"),
    path("search", views.search, name="search"),
    path("random", views.random_entry, name="random"),
]
