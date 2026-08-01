from django.forms import ModelForm
from .models import Photo, Album


class PhotoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and 'album' in self.fields:
            self.fields['album'].queryset = user.albums.all()

    class Meta:
        model = Photo
        fields = ["image","caption","album","is_public"]

    def clean(self):
        cleaned_data = super().clean()
        album = cleaned_data.get("album")
        is_public = cleaned_data.get("is_public")

        if album and not album.is_public and is_public:
            cleaned_data["is_public"] = False
            return cleaned_data
        return cleaned_data

class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description', 'is_public']


