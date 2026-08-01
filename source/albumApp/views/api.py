from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import View
from django.http import JsonResponse
from albumApp.models import Photo, Album


class  TogglePhotoFavoriteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        photo = get_object_or_404(Photo, pk=kwargs.get('pk'))
        user = request.user
        if user.favorite_photos.filter(pk=photo.pk).exists():
            user.favorite_photos.remove(photo)
            return JsonResponse({'status': 'ok', 'is_favorite': False})
        else:
            user.favorite_photos.add(photo)
            return JsonResponse({'status': 'ok', 'is_favorite': True})

class  ToggleAlbumFavoriteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        album = get_object_or_404(Album, pk=kwargs.get('pk'))
        user = request.user
        if user.favorite_albums.filter(pk=album.pk).exists():
            user.favorite_albums.remove(album)
            return JsonResponse({'status': 'ok', 'is_favorite': False})
        else:
            user.favorite_albums.add(album)
            return JsonResponse({'status': 'ok', 'is_favorite': True})