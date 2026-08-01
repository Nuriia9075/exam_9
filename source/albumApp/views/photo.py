from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from albumApp.models import Photo
from albumApp.forms import PhotoForm


# Create your views here.
class PhotoListView(ListView):
    template_name = "photos/index.html"
    model = Photo
    context_object_name = "photos"
    ordering = ["-created_at"]
    paginate_by = 3
    paginate_orphans = 1

    def get_queryset(self):
        queryset = Photo.objects.filter(is_public=True).select_related('author', 'album').order_by('-created_at')
        return queryset

class PhotoDetailView(DetailView):
    template_name = "photos/detail.html"
    model = Photo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = self.object.favorite_users.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(
                Q(is_public=True) | Q(author=self.request.user)
            )
            return queryset
        else:return queryset.filter(is_public=True)

class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = "photos/create.html"
    success_url = reverse_lazy('albumApp:photo-detail')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('albumApp:photo-detail', kwargs={'pk': self.object.pk})


class PhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = "photos/update.html"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            raise PermissionDenied("Вы не можете редактировать чужую фотографию!")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('albumApp:photo-detail', kwargs={'pk': self.object.pk})

class PhotoDeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    template_name = "photos/delete.html"
    success_url = reverse_lazy('albumApp:photo-list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            raise PermissionDenied("Вы не можете удалить чужую фотографию!")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        success_url = self.get_success_url()
        if self.object.image:
            self.object.image.delete(save=False)
        self.object.delete()
        return HttpResponseRedirect(success_url)






