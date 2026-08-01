from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q

from albumApp.forms import AlbumForm
from albumApp.models import Album
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy

class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('albumApp:album-detail', kwargs={'pk': self.object.pk})

class AlbumDetailView(LoginRequiredMixin, DetailView):
    model = Album
    template_name = 'albums/detail.html'

    def get_queryset(self):
        queryset= super().get_queryset()
        if self.request.user.is_authenticated:
            return queryset.filter(Q(is_public=True) | Q(author=self.request.user))
        return queryset.filter(is_public=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album = self.object
        photo_queryset = album.photos.all().order_by('-created_at')
        if not self.request.user == album.author:
            photo_queryset = photo_queryset.filter(is_public=True)
        paginator = Paginator(photo_queryset, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['photos'] = page_obj.object_list
        context['is_paginated'] = page_obj.has_other_pages()
        return context


class AlbumUpdateView(LoginRequiredMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/update.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author == request.user or request.user.has_perm('albumApp.change_album'):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("Это чужой альбом!")

    def form_valid(self, form):
        response = super().form_valid(form)
        if 'is_public' in form.changed_data and not form.cleaned_data['is_public']:
            self.object.photos.update(is_public=False)
        return response

    def get_success_url(self):
        return reverse_lazy('albumApp:album-detail', kwargs={'pk': self.object.pk})

class AlbumDeleteView(LoginRequiredMixin, DeleteView):
    model = Album
    template_name = 'albums/delete.html'
    success_url = reverse_lazy('albumApp:photos')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author == request.user or request.user.has_perm('albumApp.delelte_album'):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("Вы не можете удалить чужой ввлблм!")


    def form_valid(self, form):
        self.get_object().photos.all().delete()
        return super().form_valid(form)