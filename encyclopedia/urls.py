from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>/edit", views.edit, name="edit"),
    path("create", views.create, name="create"),
    path("random", views.random, name="random"),
    path("<str:name>", views.entry, name="entry")
]
