from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.file_upload),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('upload', views.upload, name='upload'),
    path('удалить видео/<int:video_id>', views.delete, name='удалить видео'),
    path('viewer/', views.main, name='viewer'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)