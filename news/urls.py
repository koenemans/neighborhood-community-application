from django.urls import path

from . import views

app_name = 'news'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<slug:slug>/', views.DetailView.as_view(), name='detail'),
    path('<int:year>/', views.YearArchiveView.as_view(), name='archive_year'),
    path('<int:year>/<int:month>', views.MonthArchiveView.as_view(month_format="%m"), name='archive_month'),
]