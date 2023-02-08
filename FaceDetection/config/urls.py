from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.http import HttpResponse
from facedetection.views import detectPersons,detections
from django.conf.urls.static import static #production ortamında otomatık olarak medıa dosyalarını yayınlamamızı sağlar
from django.conf import settings 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('facedetection/', include('facedetection.urls')),
    
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
