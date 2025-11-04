from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('skills/', views.skills_view, name='skills'),
    path('research/', views.research_view, name='research'),
    path('research/<int:pk>/', views.research_detail, name='research_detail'),
    path('experience/', views.experience_view, name='experience'),
    path('industry-index/', views.industry_index, name='industry_index'),
    path('download-cv/', views.download_cv, name='download_cv'),
    path('sitemap.xml', views.sitemap, name='sitemap'),
    path('robots.txt', views.robots_txt, name='robots'),
]
