from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("NewPage", views.newPage, name="newPage"),
    path("RandomPage", views.randomPage, name="randomPage"),
    path("EditPage/<str:title>" , views.editPage, name="editPage"),
    path("<str:search>", views.search, name="search")





]
