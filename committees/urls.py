"""URL configuration for the committees application."""

from django.urls import path

from . import views

app_name = "committees"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<slug:slug>/", views.DetailView.as_view(), name="detail"),
]
