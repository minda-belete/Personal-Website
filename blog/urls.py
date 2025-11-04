from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', views.BlogDetailView.as_view(), name='post_detail'),
    path('category/<slug:slug>/', views.blog_category, name='category'),
    path('tag/<slug:slug>/', views.blog_tag, name='tag'),
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
]
