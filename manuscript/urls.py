from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("manuscripts/", views.manuscripts, name="manuscripts"),
    path("manuscripts/<str:siglum>/", views.manuscript, name="manuscript"),
    path("toponyms/", views.toponyms, name="toponyms"),
    path("toponyms/<int:id>/", views.toponym, name="toponym"),
    path("stanzas/", views.stanzas, name="stanzas"),
]
