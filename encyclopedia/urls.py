from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("createNewPage", views.createNewPage, name="createNewPage"),
    path("edit/<str:entry>", views.editPage, name="edit"),
    path("update",views.updatePage,name="updatePage"),
    path("RandomPage", views.RandomPage, name="RandomPage")
]
