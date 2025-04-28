from django.urls import path

from . import views

app_name = 'news'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/<slug:slug>/', views.DetailView.as_view(), name='detail'),
    path('archive/', views.NewsArchiveView.as_view(), name='news_archive')
]