from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    path('', views.post_list, name='home'),    
    # <slug:slug> kısmı, URL'deki metni yakalayıp view fonksiyonuna gönderir
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('save-progress/', views.save_video_progress, name='save_video_progress'),
    
]