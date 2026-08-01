"""
URL configuration for form project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.urls import path

from albumApp.views.photo import (PhotoListView, PhotoDetailView, PhotoCreateView, PhotoUpdateView,PhotoDeleteView )
app_name = "albumApp"

urlpatterns = [
    path('', PhotoListView.as_view(), name='photos-list'),
    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='photo-detail'),
    path('update/<int:pk>/', PhotoUpdateView.as_view(), name='photo-update'),
    path('photos/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo-delete'),
    path('create/', PhotoCreateView.as_view(), name='photo-create'),
    path('photos/', PhotoListView.as_view(), name='photos')
]