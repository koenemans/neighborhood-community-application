from django.urls import path

from . import views

app_name = 'activities'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('archive/', views.ActivitiesArchiveView.as_view(), name='activities_archive'),
    path('<slug:slug>/', views.DetailView.as_view(), name='detail')
]