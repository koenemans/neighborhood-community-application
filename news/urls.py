from django.urls import path

from . import views

app_name = "news"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("archive/", views.NewsArchiveView.as_view(), name="archive"),
    path("<slug:slug>/", views.DetailView.as_view(), name="detail"),
]
