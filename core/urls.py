#coding:utf-8
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('arduino.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)