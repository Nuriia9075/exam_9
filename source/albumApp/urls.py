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

from albumApp.views.photo import (PhotoListView, PhotoDetailView, PhotoCreateView, PhotoUpdateView, PhotoDeleteView,
                                  PhotoGenerateTokenView, PhotoTokenDetailView)
from albumApp.views.album import AlbumCreateView, AlbumDetailView, AlbumUpdateView, AlbumDeleteView
from albumApp.views.api import ToggleAlbumFavoriteView,TogglePhotoFavoriteView
app_name = "albumApp"

urlpatterns = [
    path('', PhotoListView.as_view(), name='photos-list'),
    path('photos/<int:pk>/', PhotoDetailView.as_view(), name='photo-detail'),
    path('photos/<int:pk>/token/', PhotoGenerateTokenView.as_view(), name='photo-generate-token'),
    path("photos/token/<uuid:token>/",PhotoTokenDetailView.as_view(),name="photo-token",),
    path('photos/update/<int:pk>/', PhotoUpdateView.as_view(), name='photo-update'),
    path('photos/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo-delete'),
    path('photos/create/', PhotoCreateView.as_view(), name='photo-create'),
    path('photos/', PhotoListView.as_view(), name='photos'),

    path('albums/<int:pk>/', AlbumDetailView.as_view(), name='album-detail'),
    path('albums/update/<int:pk>/', AlbumUpdateView.as_view(), name='album-update'),
    path('albums/<int:pk>/delete/', AlbumDeleteView.as_view(), name='album-delete'),
    path('albums/create/', AlbumCreateView.as_view(), name='album-create'),

    path('api/photo/<int:pk>/favorite/', TogglePhotoFavoriteView.as_view(), name='api-photo-favorite'),
    path('api/album/<int:pk>/favorite/', ToggleAlbumFavoriteView.as_view(), name='api-album-favorite'),

]