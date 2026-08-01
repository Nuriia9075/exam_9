from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


def get_photo_path(instance, filename):
    return f'uploads/{instance.author.pk}/{filename}'

class Album(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums', verbose_name="Автор альбома")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата-время создания")
    is_public = models.BooleanField(default=True, verbose_name="Публичный")
    favorite_users = models.ManyToManyField(User, blank=True, related_name='favorite_albums', verbose_name="В избранном")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"

class Photo(models.Model):
    image = models.ImageField(upload_to=get_photo_path, verbose_name="Фотография")
    caption = models.CharField(max_length=255, verbose_name="Подпись")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата-время создания")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos', verbose_name="Автор")
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, blank=True, null=True, related_name='photos',
                              verbose_name="Альбом")
    is_public = models.BooleanField(default=True, verbose_name="Публичная")
    favorite_users = models.ManyToManyField(User, blank=True, related_name='favorite_photos', verbose_name="В избранном")
    token = models.CharField(max_length=50, blank=True, null=True, unique=True, verbose_name="Токен доступа")

    def __str__(self):
        return f"{self.caption} ({self.author.username})"

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"
