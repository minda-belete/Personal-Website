from django.urls import path
from . import views

app_name = 'github'

urlpatterns = [
    path('', views.RepositoryListView.as_view(), name='repository_list'),
    path('repository/<str:name>/', views.RepositoryDetailView.as_view(), name='repository_detail'),
    path('sync/', views.sync_repositories, name='sync_repositories'),
]
