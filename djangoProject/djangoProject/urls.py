"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from index import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('hello', views.hello),
    path('users/dialogs/<int:id>', views.info_id),
    path('users/dialogs/lists', views.list_id),
    path('ai/back', views.proxy_generate_request),

    path("ai/internet/back", views.connect_internet),
    # path("file/back", views.generate_bubble_sort_file),
    path("speech/text", views.speechToText),
    path("text/speech", views.generate_audio),
    path("feedback", views.feed_back),
    path("image/recognition", views.recognition_image),
]
